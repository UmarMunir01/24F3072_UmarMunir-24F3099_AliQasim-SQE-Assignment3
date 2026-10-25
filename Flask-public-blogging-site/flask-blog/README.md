# Flask Blog
This is a simple blogging website built with Flask. It includes user authentication, a comment system, and a dynamic blog post management system.

## Features
- User registration and login
- Create, read, update, and delete blog posts
- Commenting on blog posts
- User authentication with Flask-Login

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd flask-blog
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
- Set the `SECRET_KEY` and `DATABASE_URL` in your environment variables or modify the `config.py` file directly.

## Running the Application
To run the application, execute:
```
python run.py
```
The application will be available at `http://127.0.0.1:5000/`.

## Testing
To run the tests, use:
```
python -m unittest discover -s tests
```

## License
This project is licensed under the MIT License.