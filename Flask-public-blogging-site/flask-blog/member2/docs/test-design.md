# Member 2 — Task 2 test design

**Owner:** Ali Qasim  
**Assigned application modules:** `app/routes.py`, `app/auth/routes.py`, `app/__init__.py`

## `app/routes.py`

Views: `index`, `my_posts`, `others_posts`, `post_detail`, and `new_post`.

- Equivalence partitions: anonymous/authenticated visitors, public/private posts, owner/other user, valid/invalid post forms, and valid/blank/anonymous comments.
- Boundaries: missing post ID 0, empty/space-only comments, title lengths 140/141, and empty/populated post lists.
- Flask test-client checks cover rendered pages, redirects, visible posts, form feedback, and private-post 404 behavior.

## `app/auth/routes.py`

Views: `register`, `login`, and `logout`.

- Equivalence partitions: new/duplicate username, valid/invalid registration data, known/unknown user, correct/incorrect password, authenticated/anonymous logout.
- Boundaries: username lengths 2/3/64/65; password lengths 5/6; mismatched confirmation.
- UI checks cover registration/login pages, error feedback, and successful sign-in/out redirects.

## `app/__init__.py`

Functions: `create_app` and the registered user-loader callback.

- Equivalence partitions: default setup, registered blueprints, login redirect, Markdown filters, existing/unknown user IDs.
- Boundaries: valid positive user ID versus missing/non-numeric IDs. An in-memory SQLite database isolates tests from `site.db`.
- Verify routes and template filters are registered on the Flask app.

## Task 3 and Task 4

`test-cases.xlsx` documents Member 2's 10 cases. `pytest.ini`, `run_tests.py`, and `tests/conftest.py` provide this member's test suite, markers, parameterized cases, and deterministic serial ordering; `--parallel` enables xdist workers.
