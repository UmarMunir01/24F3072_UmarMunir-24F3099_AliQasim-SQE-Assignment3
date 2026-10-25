
# Flask Blog Application 📝

A modern, feature-rich blogging platform built with Flask and SQLite, featuring user authentication, markdown support, private posts, and a beautiful glassmorphism UI design.

![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

## ✨ Features

- **User Authentication** - Secure registration and login system with password hashing
- **Blog Posts** - Create, read, and manage blog posts with markdown support
- **Private Posts** - Mark posts as private to hide them from other users
- **Comments** - Interactive commenting system for engaging with content
- **Glassmorphism UI** - Modern, eye-catching authentication pages with animated gradients
- **Responsive Design** - Works beautifully on desktop and mobile devices
- **Markdown Support** - Write posts using markdown syntax with syntax highlighting

## 🛠️ Technologies Used

- **Backend**: Flask 3.0, Flask-Login, Flask-WTF
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Werkzeug password hashing
- **Frontend**: HTML5, CSS3 (Glassmorphism design), Jinja2 templates
- **Markdown**: Python-Markdown with extensions

## 📁 Project Structure

```
flask-blog/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models (User, Post, Comment)
│   ├── routes.py             # Main application routes
│   ├── forms.py              # WTForms form definitions
│   ├── markdown_utils.py     # Markdown processing utilities
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py         # Authentication routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Application styles
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html         # Base template
│       ├── index.html        # Home page
│       ├── post_detail.html  # Individual post view
│       ├── post_form.html    # Create/edit post form
│       └── auth/
│           ├── base_auth.html # Auth pages base template
│           ├── login.html     # Login page
│           └── register.html  # Registration page
├── tests/
│   ├── test_auth.py          # Authentication tests
│   └── test_posts.py         # Post functionality tests
├── .env                       # Environment variables (not in repo)
├── .gitignore
├── config.py                  # Configuration settings
├── create_db.py              # Database initialization script
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/Maderana/Flask-public-blogging-site.git
   cd flask-blog
   ```

2. **Create and activate a virtual environment**
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Create environment variables**
   
   Create a `.env` file in the project root directory with the following variables:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///site.db
   ```
   
   **Generate a secure SECRET_KEY** using Python:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as your `SECRET_KEY` value.

5. **Initialize the database**
   ```
   python create_db.py
   ```
   This will create the `site.db` SQLite database file with all necessary tables.

6. **Run the application**
   ```
   python run.py
   ```
   Or use Flask's built-in command:
   ```
   flask run
   ```

7. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage

### Creating an Account

1. Navigate to the registration page by clicking "Sign up"
2. Choose a unique username and secure password
3. Click "Create Account" to register

### Writing Posts

1. Log in to your account
2. Click "New Post" in the navigation
3. Write your post title and content (markdown supported)
4. Check "Make this post private" if you want only you to see it
5. Click "Submit" to publish

### Managing Privacy

- **Public Posts**: Visible to all users
- **Private Posts**: Only visible to you when logged in
- Toggle privacy when creating or editing posts

### Commenting

- Click on any post title to view the full post
- Scroll down to the comments section
- Add your comment and click "Submit"

## 🧪 Testing

Run the test suite using:
```
pytest
```

Or run specific test files:
```
pytest tests/test_auth.py
pytest tests/test_posts.py
```

## 🔧 Configuration

Edit `config.py` to modify application settings:

- `SECRET_KEY`: Used for session management and CSRF protection
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disable to reduce overhead

## 📦 Dependencies

Key dependencies (see `requirements.txt` for full list):

- Flask - Web framework
- Flask-SQLAlchemy - Database ORM
- Flask-Login - User session management
- Flask-WTF - Form handling and validation
- Werkzeug - Password hashing
- Markdown - Content rendering
- Pygments - Code syntax highlighting

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- None currently reported

## 🛣️ Roadmap

- [ ] Post editing functionality
- [ ] Post deletion with confirmation
- [ ] User profile pages
- [ ] Post categories/tags
- [ ] Search functionality
- [ ] Rich text editor
- [ ] Email notifications
- [ ] Social media sharing

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Maderana - [My GitHub Profile](https://github.com/Maderana)

## 🙏 Acknowledgments

- Flask documentation and community
- Markdown and Pygments libraries

## 📞 Support

For support, please open an issue on GitHub or contact [maderana007@gmail.com]

---

**Note**: This is a development version. For production deployment, ensure you:
- Use a production-grade database (PostgreSQL, MySQL)
- Set up proper environment variables
- Enable HTTPS
- Configure proper security headers
- Use a production WSGI server (Gunicorn, uWSGI)
```
