# Flask Public Blogging Site

A Flask and SQLite blogging application with account registration and login, public and private posts, comments, and Markdown rendering with HTML sanitization.

## Prerequisites

- Python and pip
- PowerShell on Windows, or a shell with Python virtual environment support

## Run locally

Run these commands from the repository root. The application is inside `Flask-public-blogging-site/flask-blog`.

1. Enter the application folder and create a virtual environment:

   ```powershell
   cd .\Flask-public-blogging-site\flask-blog
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS or Linux, activate it with `source .venv/bin/activate` instead.

2. Install the application and its additional runtime dependencies:

   ```shell
   python -m pip install -r requirements.txt
   python -m pip install -r member1/requirements-assignment3.txt
   ```

3. Set `SECRET_KEY` in the existing `.env` file (or create that file in `flask-blog`). You can generate a value with:

   ```shell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   `SQLALCHEMY_DATABASE_URI` is optional. If omitted, the app uses the SQLite database at `flask-blog/site.db`.

4. Create the database tables:

   ```shell
   python create_db.py
   ```

5. Start the development server:

   ```shell
   python run.py
   ```

6. Open <http://127.0.0.1:5000/> in your browser. Stop the server with `Ctrl+C`.

## Tests

From `flask-blog`, run the main test suite with:

```shell
python -m pytest
```

To run the additional Member 1 suite, install its test dependencies and use its runner:

```shell
python member1/run_tests.py
```
