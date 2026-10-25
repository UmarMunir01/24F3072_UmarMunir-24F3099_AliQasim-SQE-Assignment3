import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    basedir = os.path.abspath(os.path.dirname(__file__))

    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET_KEY = os.getenv('SECRET_KEY')
    print(f"Loaded SECRET_KEY: {SECRET_KEY}")  # Debug line to verify loading
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') + os.path.join(basedir, 'site.db')
    
    # If environment variable contains a full URI use it, otherwise build a sqlite path.
    env_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    if env_uri and env_uri.strip() != '':
        # allow providing full URI like "sqlite:///C:/path/site.db" or a prefix like "sqlite:///"
        if env_uri.endswith('/') and env_uri.count('/') == 3:
            SQLALCHEMY_DATABASE_URI = env_uri + os.path.join(basedir, 'site.db')
        else:
            SQLALCHEMY_DATABASE_URI = env_uri
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')

    print(f"Using SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")  # Debug line to verify loading
    SQLALCHEMY_TRACK_MODIFICATIONS = False