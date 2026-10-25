# Member 1 contribution — Umar Munir

This folder contains Member 1's independent files for Assignment 3 Tasks 2–4.

## Assigned modules

- `app/forms.py`
- `app/markdown_utils.py`
- `app/models.py`

## Contents

- `docs/test-design.md`: Task 2 equivalence partitions, boundaries, and UI checks.
- `docs/test-cases.xlsx`: Task 3 register with 10 Member 1 cases.
- `tests/`: Member 1 automated tests and isolated fixtures for Task 4.
- `tests/data/registration_cases.csv`: seven external registration cases used directly by the parameterized form test.
- `pytest.ini`, `run_tests.py`, `requirements-assignment3.txt`: markers, ordered/grouped execution, optional parallel execution, and extra app dependencies.

## Add and run in the Flask app repository

Copy the `member1` folder to the root of `flask-blog/`, install the app requirements and `member1/requirements-assignment3.txt`, then run:

```powershell
python member1/run_tests.py
python member1/run_tests.py -- -m forms
python member1/run_tests.py --parallel
```

