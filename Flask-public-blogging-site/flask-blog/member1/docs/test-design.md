# Member 1 — Task 2 test design

**Owner:** Umar Munir  
**Assigned application modules:** `app/forms.py`, `app/markdown_utils.py`, `app/models.py`

## `app/forms.py`

Classes: `RegistrationForm`, `LoginForm`, and `PostForm`.

- Equivalence partitions: required and missing fields, matching and mismatching password confirmation, checked and unchecked private-post option, valid and invalid field values.
- Boundary values: registration username lengths 2, 3, 64, and 65; registration password lengths 5 and 6; post title lengths 140 and 141.
- The seven external CSV rows drive registration boundary and confirmation checks. Flask test-client checks cover registration and form feedback.

## `app/markdown_utils.py`

Functions: `markdown_to_html` and `markdown_title`.

- Equivalence partitions: empty input, plain text, emphasis, headings, fenced code, tables, links, and unsafe HTML or URL schemes.
- Boundaries: empty and one-character input; single-line and multiline input; markup with and without an enclosing paragraph.
- Check HTML rendering, title paragraph removal, and sanitization of scripts and unsafe links.

## `app/models.py`

Classes: `User`, `Post`, and `Comment`.

- Equivalence partitions: correct, wrong, and empty passwords; public/private posts; authenticated/anonymous comments; linked/unlinked author records.
- Boundaries: empty/max-length values, password hash replacement, and timestamp/default behavior at persistence.
- Check repr methods, relationships, defaults, persistence, and password hashing.

## Task 3 and Task 4

`test-cases.xlsx` documents Member 1's 10 cases. The external CSV is read by the parameterized registration test. `pytest.ini`, `run_tests.py`, and `tests/conftest.py` provide the member suite, markers, parameter expansion, and deterministic serial ordering; `--parallel` enables xdist workers.
