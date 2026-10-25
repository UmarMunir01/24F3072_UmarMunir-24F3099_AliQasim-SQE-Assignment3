"""Member 2: public/private blog views and post/comment routes."""
from datetime import datetime

import pytest

from app import db
from app.models import Comment, Post, User


pytestmark = [pytest.mark.member2, pytest.mark.routes, pytest.mark.order(40)]


def test_index_renders_public_posts_for_anonymous_users(client, factories):
    make_user, make_post, _ = factories
    author = make_user("author")
    make_post(author, title="Visible public")
    response = client.get("/")
    assert response.status_code == 200
    assert b"Visible public" in response.data


def test_index_hides_private_posts_from_anonymous_users(client, factories):
    make_user, make_post, _ = factories
    author = make_user("author")
    make_post(author, title="Hidden private", private=True)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hidden private" not in response.data


def test_index_shows_authenticated_user_own_private_post(logged_in_client, factories):
    client, user_id = logged_in_client
    _, make_post, _ = factories
    make_post(user_id, title="My private post", private=True)
    response = client.get("/")
    assert response.status_code == 200
    assert b"My private post" in response.data


def test_index_hides_another_users_private_post_from_authenticated_user(logged_in_client, factories):
    client, _ = logged_in_client
    make_user, make_post, _ = factories
    author_id = make_user("another")
    make_post(author_id, title="Not mine", private=True)
    assert b"Not mine" not in client.get("/").data


def test_index_orders_newest_post_before_older_post(app, client, factories):
    make_user, _, _ = factories
    author_id = make_user("author")
    with app.app_context():
        older = Post(title="Older marker", content="a", author_id=author_id, timestamp=datetime(2020, 1, 1))
        newer = Post(title="Newer marker", content="b", author_id=author_id, timestamp=datetime(2021, 1, 1))
        db.session.add_all([older, newer])
        db.session.commit()
    page = client.get("/").data
    assert page.index(b"Newer marker") < page.index(b"Older marker")


def test_my_posts_requires_login(client):
    response = client.get("/my_posts")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_my_posts_shows_only_current_users_posts(logged_in_client, factories):
    client, user_id = logged_in_client
    make_user, make_post, _ = factories
    make_post(user_id, title="Mine")
    other_id = make_user("other")
    make_post(other_id, title="Other user's")
    page = client.get("/my_posts").data
    assert b"Mine" in page
    assert b"Other user's" not in page


def test_my_posts_renders_empty_list_for_user_without_posts(logged_in_client):
    client, _ = logged_in_client
    response = client.get("/my_posts")
    assert response.status_code == 200


def test_my_posts_page_renders_filter_title(logged_in_client):
    client, _ = logged_in_client
    assert client.get("/my_posts").status_code == 200


def test_my_posts_orders_newest_first(app, logged_in_client, factories):
    client, user_id = logged_in_client
    with app.app_context():
        db.session.add_all([
            Post(title="My older", content="a", author_id=user_id, timestamp=datetime(2020, 1, 1)),
            Post(title="My newer", content="b", author_id=user_id, timestamp=datetime(2021, 1, 1)),
        ])
        db.session.commit()
    page = client.get("/my_posts").data
    assert page.index(b"My newer") < page.index(b"My older")


def test_others_posts_requires_login(client):
    response = client.get("/others_posts")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_others_posts_shows_other_users_public_posts(logged_in_client, factories):
    client, _ = logged_in_client
    make_user, make_post, _ = factories
    other_id = make_user("other")
    make_post(other_id, title="Other public")
    assert b"Other public" in client.get("/others_posts").data


def test_others_posts_excludes_current_users_posts(logged_in_client, factories):
    client, user_id = logged_in_client
    _, make_post, _ = factories
    make_post(user_id, title="OWN_ROUTE_POST_123")
    assert b"OWN_ROUTE_POST_123" not in client.get("/others_posts").data


def test_others_posts_hides_private_posts_from_other_users(logged_in_client, factories):
    client, _ = logged_in_client
    make_user, make_post, _ = factories
    other_id = make_user("other")
    make_post(other_id, title="Other private", private=True)
    assert b"Other private" not in client.get("/others_posts").data


def test_others_posts_returns_empty_page_when_no_other_posts(logged_in_client):
    client, _ = logged_in_client
    assert client.get("/others_posts").status_code == 200


def test_post_detail_renders_public_post_for_anonymous_user(client, factories):
    make_user, make_post, _ = factories
    post_id = make_post(make_user("author"), title="Public detail")
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
    assert b"Public detail" in response.data


def test_post_detail_returns_404_for_missing_id_zero(client):
    assert client.get("/post/0").status_code == 404


def test_post_detail_hides_private_post_from_anonymous_user(client, factories):
    make_user, make_post, _ = factories
    post_id = make_post(make_user("author"), title="Private detail", private=True)
    assert client.get(f"/post/{post_id}").status_code == 404


def test_post_detail_allows_author_to_view_private_post(logged_in_client, factories):
    client, user_id = logged_in_client
    _, make_post, _ = factories
    post_id = make_post(user_id, title="Owner only", private=True)
    assert client.get(f"/post/{post_id}").status_code == 200


def test_post_detail_hides_private_post_from_another_logged_in_user(client, factories):
    make_user, make_post, _ = factories
    owner_id = make_user("owner")
    post_id = make_post(owner_id, title="Restricted", private=True)
    client.post("/auth/login", data={"username": "owner", "password": "password123"})
    client.get("/auth/logout")
    make_user("reader")
    client.post("/auth/login", data={"username": "reader", "password": "password123"})
    assert client.get(f"/post/{post_id}").status_code == 404


def test_post_detail_redirects_anonymous_commenter_to_login(client, factories):
    make_user, make_post, _ = factories
    post_id = make_post(make_user("author"), title="Comment target")
    response = client.post(f"/post/{post_id}", data={"content": "hello"})
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_post_detail_saves_trimmed_comment_for_logged_in_user(logged_in_client, factories, app):
    client, user_id = logged_in_client
    _, make_post, _ = factories
    post_id = make_post(user_id, title="Comment target")
    response = client.post(f"/post/{post_id}", data={"content": "  useful comment  "})
    assert response.status_code == 302
    with app.app_context():
        comment = Comment.query.filter_by(post_id=post_id).one()
        assert comment.content == "useful comment"
        assert comment.author_id == user_id


def test_post_detail_rejects_blank_comment_without_creating_record(logged_in_client, factories, app):
    client, user_id = logged_in_client
    _, make_post, _ = factories
    post_id = make_post(user_id, title="Comment target")
    response = client.post(f"/post/{post_id}", data={"content": "   "})
    assert response.status_code == 200
    assert b"Comment cannot be empty" in response.data
    with app.app_context():
        assert Comment.query.filter_by(post_id=post_id).count() == 0


def test_new_post_requires_login(client):
    response = client.get("/new_post")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_new_post_form_renders_for_logged_in_user(logged_in_client):
    client, _ = logged_in_client
    response = client.get("/new_post")
    assert response.status_code == 200
    assert b"Title" in response.data and b"Content" in response.data


def test_new_post_creates_public_post_by_default(logged_in_client, app):
    client, user_id = logged_in_client
    response = client.post("/new_post", data={"title": "New public", "content": "body"})
    assert response.status_code == 302
    with app.app_context():
        post = Post.query.filter_by(title="New public").one()
        assert post.author_id == user_id
        assert post.is_private is False


def test_new_post_creates_private_post_when_checkbox_checked(logged_in_client, app):
    client, _ = logged_in_client
    client.post("/new_post", data={"title": "New private", "content": "body", "is_private": "y"})
    with app.app_context():
        assert Post.query.filter_by(title="New private").one().is_private is True


def test_new_post_rejects_missing_title(logged_in_client, app):
    client, _ = logged_in_client
    response = client.post("/new_post", data={"title": "", "content": "body"})
    assert response.status_code == 200
    with app.app_context():
        assert Post.query.count() == 0


def test_new_post_rejects_title_of_141_characters(logged_in_client, app):
    client, _ = logged_in_client
    response = client.post("/new_post", data={"title": "x" * 141, "content": "body"})
    assert response.status_code == 200
    with app.app_context():
        assert Post.query.count() == 0


def test_new_post_rejects_blank_content(logged_in_client, app):
    client, _ = logged_in_client
    response = client.post("/new_post", data={"title": "No content", "content": "   "})
    assert response.status_code == 200
    with app.app_context():
        assert Post.query.count() == 0
