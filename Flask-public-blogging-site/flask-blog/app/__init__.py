from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

     # redirect for @login_required
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # register markdown filter (import here to avoid circular imports)
    from app.markdown_utils import markdown_to_html, markdown_title
    app.jinja_env.filters['markdown_to_html'] = markdown_to_html
    app.jinja_env.filters['markdown_title'] = markdown_title

    from app.routes import main
    from app.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app

# optional: register user loader if models.User exists
try:
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
except Exception:
    # models may not be ready yet while editing - ignore for now
    pass