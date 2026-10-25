"""Member 1: form validation, including external CSV boundary cases."""
import csv
from pathlib import Path

import pytest

from app.forms import LoginForm, PostForm, RegistrationForm


pytestmark = [pytest.mark.member1, pytest.mark.forms, pytest.mark.order(10)]

CSV_PATH = Path(__file__).parent / "data" / "registration_cases.csv"
with CSV_PATH.open(newline="", encoding="utf-8") as csv_file:
    REGISTRATION_CASES = list(csv.DictReader(csv_file))


@pytest.mark.parametrize("case", REGISTRATION_CASES, ids=lambda row: row["case_id"])
@pytest.mark.csv_data
def test_registration_form_uses_external_csv_cases(app, case):
    with app.test_request_context("/"):
        form = RegistrationForm(data={
            "username": case["username"],
            "password": case["password"],
            "password2": case["password2"],
        })
        assert form.validate() is (case["expected_valid"].lower() == "true"), case["description"]


def test_registration_form_requires_username_and_password(app):
    with app.test_request_context("/"):
        form = RegistrationForm(data={})
        assert not form.validate()
        assert {"username", "password", "password2"}.issubset(form.errors)


def test_login_form_accepts_nonempty_credentials(app):
    with app.test_request_context("/"):
        assert LoginForm(data={"username": "alice", "password": "x"}).validate()


@pytest.mark.parametrize("data", [{"username": "", "password": "x"}, {"username": "alice", "password": ""}, {}])
def test_login_form_requires_both_fields(app, data):
    with app.test_request_context("/"):
        form = LoginForm(data=data)
        assert not form.validate()
        assert {"username", "password"}.intersection(form.errors)


def test_login_form_does_not_apply_registration_password_minimum(app):
    with app.test_request_context("/"):
        assert LoginForm(data={"username": "a", "password": "x"}).validate()


def test_post_form_accepts_title_at_140_character_boundary(app):
    with app.test_request_context("/"):
        form = PostForm(data={"title": "t" * 140, "content": "body"})
        assert form.validate()


def test_post_form_rejects_title_above_140_character_boundary(app):
    with app.test_request_context("/"):
        form = PostForm(data={"title": "t" * 141, "content": "body"})
        assert not form.validate()
        assert "title" in form.errors


@pytest.mark.parametrize("content", ["", "   "])
def test_post_form_requires_nonblank_content(app, content):
    with app.test_request_context("/"):
        form = PostForm(data={"title": "A title", "content": content})
        assert not form.validate()
        assert "content" in form.errors


def test_post_form_reads_private_checkbox(app):
    with app.test_request_context("/"):
        form = PostForm(data={"title": "Private", "content": "body", "is_private": True})
        assert form.validate()
        assert form.is_private.data is True


def test_post_form_defaults_private_checkbox_to_false(app):
    with app.test_request_context("/"):
        form = PostForm(data={"title": "Public", "content": "body"})
        assert form.validate()
        assert form.is_private.data is False
