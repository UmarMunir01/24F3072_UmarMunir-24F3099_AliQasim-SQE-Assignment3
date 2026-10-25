"""Member 2: Flask application factory and registered user loader."""
import pytest

from app import create_app, login_manager
from app.models import User


pytestmark = [pytest.mark.member2, pytest.mark.app_factory, pytest.mark.order(60)]


def test_create_app_returns_flask_application(app):
    from flask import Flask
    assert isinstance(app, Flask)


def test_create_app_registers_main_and_auth_blueprints(app):
    assert "main" in app.blueprints
    assert "auth" in app.blueprints


def test_create_app_registers_expected_routes(app):
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert {"/", "/new_post", "/auth/login", "/auth/register"}.issubset(rules)


def test_create_app_installs_markdown_template_filters(app):
    assert callable(app.jinja_env.filters["markdown_to_html"])
    assert callable(app.jinja_env.filters["markdown_title"])


def test_create_app_sets_login_redirect_view(app):
    assert login_manager.login_view == "auth.login"


def test_user_loader_returns_existing_user(app, factories):
    make_user, _, _ = factories
    user_id = make_user("loader-user")
    with app.app_context():
        loaded = login_manager._user_callback(str(user_id))
        assert loaded is not None
        assert loaded.username == "loader-user"


@pytest.mark.parametrize("user_id", ["0", "-1", "999999", "2147483647"], ids=["zero", "negative", "unknown", "large"])
def test_user_loader_returns_none_for_unknown_id(app, user_id):
    with app.app_context():
        assert login_manager._user_callback(user_id) is None


def test_create_app_uses_isolated_database_configuration(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
