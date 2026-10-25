# Member 2 contribution — Ali Qasim

This folder contains Member 2's independent files for Assignment 3 Tasks 2–4.

## Assigned modules

- `app/routes.py`
- `app/auth/routes.py`
- `app/__init__.py`

## Contents

- `docs/test-design.md`: Task 2 equivalence partitions, boundaries, and UI checks.
- `docs/test-cases.xlsx`: Task 3 register with 10 Member 2 cases.
- `tests/`: Member 2 automated tests and isolated fixtures for Task 4.
- `pytest.ini`, `run_tests.py`, `requirements-assignment3.txt`: markers, ordered/grouped execution, optional parallel execution, and extra app dependencies.

## Add and run in the Flask app repository

Copy the `member2` folder to the root of `flask-blog/`, install the app requirements and `member2/requirements-assignment3.txt`, then run:

```powershell
python member2/run_tests.py
python member2/run_tests.py -- -m auth
python member2/run_tests.py --parallel
```
 

