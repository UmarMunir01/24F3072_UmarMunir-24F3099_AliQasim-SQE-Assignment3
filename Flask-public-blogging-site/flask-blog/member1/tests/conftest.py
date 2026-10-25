"""Shared isolated fixtures and deterministic serial test ordering."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


# When copied into <project>/tests/assignment3 this resolves to the project root.
# APP_ROOT lets us verify the drop-in suite against a separate local clone.
PROJECT_ROOT = Path(os.environ.get("APP_ROOT", Path(__file__).resolve().parents[2])).resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Avoid loading or printing the developer's real secret/database configuration.
os.environ.setdefault("SECRET_KEY", "assignment-test-secret")
os.environ.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")

from app import create_app, db  # noqa: E402
from app.models import Comment, Post, User  # noqa: E402


@pytest.fixture
def app():
    flask_app = create_app()
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="assignment-test-secret",
    )
    with flask_app.app_context():
        db.create_all()
    yield flask_app
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def factories(app):
    """Factories return persisted IDs so tests can safely leave app contexts."""
    def make_user(username="alice", password="password123"):
        with app.app_context():
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user.id

    def make_post(author_id, title="Sample post", content="Body", private=False):
        with app.app_context():
            post = Post(
                title=title, content=content, author_id=author_id,
                is_private=private,
            )
            db.session.add(post)
            db.session.commit()
            return post.id

    def make_comment(post_id, author_id=None, content="A comment"):
        with app.app_context():
            comment = Comment(
                post_id=post_id, author_id=author_id, content=content,
            )
            db.session.add(comment)
            db.session.commit()
            return comment.id

    return make_user, make_post, make_comment


@pytest.fixture
def logged_in_client(client, factories):
    make_user, _, _ = factories
    user_id = make_user()
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "password123"},
    )
    assert response.status_code == 302
    return client, user_id


def pytest_collection_modifyitems(items):
    """Sort by declared order markers; stable collection order breaks ties.

    This is a deterministic serial ordering. Parallel workers can finish in any
    order, so use run_assignment3.py without --parallel when exact order matters.
    """
    indexed = list(enumerate(items))

    def order_key(pair):
        original_index, item = pair
        marker = item.get_closest_marker("order")
        value = marker.args[0] if marker and marker.args else 10_000
        return value, original_index

    items[:] = [item for _, item in sorted(indexed, key=order_key)]
