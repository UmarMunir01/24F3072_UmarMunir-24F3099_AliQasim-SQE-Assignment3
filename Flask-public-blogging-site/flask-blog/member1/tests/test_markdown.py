"""Member 1: Markdown rendering, title rendering, and sanitization."""
import pytest

from app.markdown_utils import markdown_title, markdown_to_html


pytestmark = [pytest.mark.member1, pytest.mark.markdown, pytest.mark.order(20)]


@pytest.mark.parametrize("value", [None, ""], ids=["none", "empty"])
def test_markdown_to_html_returns_empty_markup_for_empty_input(value):
    assert str(markdown_to_html(value)) == ""


def test_markdown_to_html_renders_heading_and_emphasis():
    output = str(markdown_to_html("# Heading\n\n**bold**"))
    assert "<h1>Heading</h1>" in output
    assert "<strong>bold</strong>" in output


def test_markdown_to_html_renders_fenced_code():
    output = str(markdown_to_html("```python\nprint('hi')\n```"))
    assert "<pre>" in output and "print" in output


def test_markdown_to_html_renders_table():
    output = str(markdown_to_html("| A | B |\n|---|---|\n| 1 | 2 |"))
    assert "<table>" in output and "<td>1</td>" in output


def test_markdown_to_html_strips_script_markup():
    output = str(markdown_to_html("<script>alert('x')</script>safe"))
    assert "<script" not in output.lower()
    # Bleach removes the executable element; its text remains ordinary text.
    assert "alert('x')" in output
    assert "safe" in output


def test_markdown_to_html_removes_javascript_url_scheme():
    output = str(markdown_to_html("[bad](javascript:alert(1))"))
    assert "javascript:" not in output.lower()


@pytest.mark.parametrize("value", [None, ""], ids=["none", "empty"])
def test_markdown_title_returns_empty_markup_for_empty_input(value):
    assert str(markdown_title(value)) == ""


def test_markdown_title_renders_plain_text_without_outer_paragraph():
    assert str(markdown_title("A short title")) == "A short title"


def test_markdown_title_preserves_allowed_inline_formatting():
    output = str(markdown_title("A **bold** `title`"))
    assert "<strong>bold</strong>" in output
    assert "<code>title</code>" in output
    assert not output.startswith("<p>")


def test_markdown_title_strips_script_markup():
    output = str(markdown_title("<script>alert(1)</script>Title"))
    assert "<script" not in output.lower()


def test_markdown_title_strips_paragraph_tags_from_multiline_input():
    output = str(markdown_title("first\n\nsecond"))
    assert "<p>" not in output
    assert "</p>" not in output
    assert "first" in output and "second" in output


def test_markdown_title_keeps_safe_http_link():
    output = str(markdown_title("[site](https://example.com)"))
    assert "https://example.com" in output
