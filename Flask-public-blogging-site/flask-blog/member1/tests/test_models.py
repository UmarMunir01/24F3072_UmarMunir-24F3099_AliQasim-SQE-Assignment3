"""Member 1: User, Post, and Comment SQLAlchemy model behavior."""
import pytest

from app import db
from app.models import Comment, Post, User


pytestmark = [pytest.mark.member1, pytest.mark.models, pytest.mark.order(30)]


def test_user_set_password_stores_a_hash(app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("secret123")
        assert user.password_hash != "secret123"
        assert user.password_hash


def test_user_password_hash_is_salted(app):
    with app.app_context():
        first, second = User(username="a"), User(username="b")
        first.set_password("same-secret")
        second.set_password("same-secret")
        assert first.password_hash != second.password_hash


def test_user_check_password_accepts_correct_password(app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("secret123")
        assert user.check_password("secret123") is True


@pytest.mark.parametrize("candidate", ["wrong", "", "secret12"], ids=["wrong", "empty", "near-match"])
def test_user_check_password_rejects_incorrect_passwords(app, candidate):
    with app.app_context():
        user = User(username="alice")
        user.set_password("secret123")
        assert user.check_password(candidate) is False


@pytest.mark.parametrize("username", ["alice", "A B", "user-1", "u" * 64, "ümlaut"], ids=["simple", "space", "hyphen", "max-length", "unicode"])
def test_user_repr_contains_username(app, username):
    with app.app_context():
        assert repr(User(username=username)) == f"<User {username}>"


def test_user_password_can_be_changed(app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("before1")
        user.set_password("after22")
        assert user.check_password("after22")
        assert not user.check_password("before1")


def test_user_set_password_accepts_empty_string_as_hashable_input(app):
    with app.app_context():
        user = User(username="empty-password")
        user.set_password("")
        assert user.password_hash
        assert user.check_password("")


def test_user_set_password_accepts_unicode_password(app):
    with app.app_context():
        user = User(username="unicode-password")
        user.set_password("пароль🔐")
        assert user.check_password("пароль🔐")


def test_post_private_default_is_false_after_insert(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Public", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        assert post.is_private is False


def test_post_can_be_marked_private(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Private", content="Body", author_id=user.id, is_private=True)
        db.session.add(post)
        db.session.flush()
        assert post.is_private is True


def test_post_timestamp_default_is_set_when_persisted(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Timed", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        assert post.timestamp is not None


@pytest.mark.parametrize("title", ["A title", "", "spaces in title", "emoji 📝", "x" * 140], ids=["normal", "empty", "spaces", "unicode", "max-length"])
def test_post_repr_contains_title_and_author_relationship_works(app, title):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title=title, content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        assert repr(post) == f"<Post {title}>"
        assert post.author.username == "author"


def test_post_preserves_body_content_when_persisted(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Body", content="# heading\n\n**bold**", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        assert post.content == "# heading\n\n**bold**"


@pytest.mark.parametrize("content", ["Hi", "", "spaces are okay", "emoji 💬", "x" * 100], ids=["normal", "empty", "spaces", "unicode", "long"])
def test_comment_repr_contains_comment_and_post_ids(app, content):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Post", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        comment = Comment(content=content, post_id=post.id, author_id=user.id)
        db.session.add(comment)
        db.session.flush()
        assert repr(comment) == f"<Comment {comment.id} on post {post.id}>"


def test_comment_can_have_anonymous_author(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Post", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        comment = Comment(content="Anonymous", post_id=post.id, author_id=None)
        db.session.add(comment)
        db.session.flush()
        assert comment.author_id is None
        assert comment.post.title == "Post"


def test_comment_timestamp_default_is_set_when_persisted(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Post", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        comment = Comment(content="Comment", post_id=post.id, author_id=user.id)
        db.session.add(comment)
        db.session.flush()
        assert comment.timestamp is not None


def test_comment_content_is_persisted_verbatim(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Post", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        comment = Comment(content="  raw text  ", post_id=post.id, author_id=user.id)
        db.session.add(comment)
        db.session.flush()
        assert comment.content == "  raw text  "


def test_user_post_and_comment_relationships_persist(app):
    with app.app_context():
        user = User(username="author")
        user.set_password("password")
        db.session.add(user)
        db.session.flush()
        post = Post(title="Post", content="Body", author_id=user.id)
        db.session.add(post)
        db.session.flush()
        comment = Comment(content="Comment", post_id=post.id, author_id=user.id)
        db.session.add(comment)
        db.session.commit()
        assert user.posts.count() == 1
        assert user.comments.count() == 1
        assert post.comments.count() == 1
