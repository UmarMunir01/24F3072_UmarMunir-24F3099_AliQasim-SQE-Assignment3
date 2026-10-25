"""Member 2: account registration, login, and logout routes."""
import pytest

from app import db
from app.models import User


pytestmark = [pytest.mark.member2, pytest.mark.auth, pytest.mark.order(50)]


def test_register_page_renders_ui(client):
    response = client.get("/auth/register")
    assert response.status_code == 200
    assert b"Register" in response.data or b"Join Us" in response.data


def test_register_creates_user_and_redirects_to_login(client, app):
    response = client.post("/auth/register", data={
        "username": "newuser", "password": "secret123", "password2": "secret123",
    })
    assert response.status_code == 302
    assert "/auth/login" in response.location
    with app.app_context():
        assert User.query.filter_by(username="newuser").one() is not None


def test_register_rejects_duplicate_username(client, app):
    with app.app_context():
        user = User(username="taken")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    response = client.post("/auth/register", data={
        "username": "taken", "password": "secret123", "password2": "secret123",
    })
    assert response.status_code == 200
    assert b"Username already taken" in response.data


@pytest.mark.parametrize("username", ["ab", "a" * 65], ids=["below-min", "above-max"])
def test_register_rejects_username_outside_boundaries(client, username):
    response = client.post("/auth/register", data={
        "username": username, "password": "secret123", "password2": "secret123",
    })
    assert response.status_code == 200
    assert b"Registration error" in response.data


def test_register_accepts_username_at_maximum_length(client, app):
    username = "u" * 64
    response = client.post("/auth/register", data={
        "username": username, "password": "secret123", "password2": "secret123",
    })
    assert response.status_code == 302
    with app.app_context():
        assert User.query.filter_by(username=username).first() is not None


def test_register_rejects_password_below_minimum(client):
    response = client.post("/auth/register", data={
        "username": "newuser", "password": "12345", "password2": "12345",
    })
    assert response.status_code == 200
    assert b"Registration error" in response.data


def test_register_accepts_password_at_six_character_boundary(client):
    response = client.post("/auth/register", data={
        "username": "newuser", "password": "123456", "password2": "123456",
    })
    assert response.status_code == 302


def test_register_rejects_confirmation_mismatch(client):
    response = client.post("/auth/register", data={
        "username": "newuser", "password": "secret123", "password2": "different",
    })
    assert response.status_code == 200
    assert b"Registration error" in response.data


def test_register_rejects_missing_required_fields(client):
    response = client.post("/auth/register", data={})
    assert response.status_code == 200
    assert b"Registration error" in response.data


def test_login_page_renders_ui(client):
    response = client.get("/auth/login")
    assert response.status_code == 200
    assert b"Login" in response.data or b"Welcome Back" in response.data


def test_login_accepts_valid_credentials_and_redirects(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    response = client.post("/auth/login", data={"username": "alice", "password": "password123"})
    assert response.status_code == 302
    assert response.location.endswith("/")


@pytest.mark.parametrize(
    "username,password",
    [("missing", "password123"), ("alice", "wrongpass")],
    ids=["unknown-user", "wrong-password"],
)
def test_login_rejects_unknown_user_or_wrong_password(client, app, username, password):
    if username == "alice":
        with app.app_context():
            user = User(username="alice")
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()
    response = client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200
    assert b"Login failed" in response.data


@pytest.mark.parametrize("data", [{"username": "", "password": "x"}, {"username": "alice", "password": ""}, {}])
def test_login_shows_validation_feedback_for_missing_fields(client, data):
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert b"Login error" in response.data


def test_login_honors_next_query_parameter_for_protected_page(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    response = client.post("/auth/login?next=%2Fmy_posts", data={
        "username": "alice", "password": "password123",
    })
    assert response.status_code == 302
    assert response.location.endswith("/my_posts")


def test_logout_requires_login(client):
    response = client.get("/auth/logout")
    assert response.status_code == 302
    assert "/auth/login" in response.location


def test_logout_clears_authenticated_session(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    client.post("/auth/login", data={"username": "alice", "password": "password123"})
    response = client.get("/auth/logout")
    assert response.status_code == 302
    with client.session_transaction() as session:
        assert "_user_id" not in session


def test_logout_redirects_to_home(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    client.post("/auth/login", data={"username": "alice", "password": "password123"})
    assert client.get("/auth/logout").location.endswith("/")


def test_logout_displays_confirmation_message(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    client.post("/auth/login", data={"username": "alice", "password": "password123"})
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"logged out" in response.data.lower()


def test_user_can_log_in_again_after_logout(client, app):
    with app.app_context():
        user = User(username="alice")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
    client.post("/auth/login", data={"username": "alice", "password": "password123"})
    client.get("/auth/logout")
    response = client.post("/auth/login", data={"username": "alice", "password": "password123"})
    assert response.status_code == 302
