import pytest
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


def test_register_page_loads(client):
    """Test that the registration page loads successfully."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Join Us!' in response.data or b'Register' in response.data


def test_register_user(client, app):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify user was created in database
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.username == 'testuser'


def test_register_duplicate_username(client, app):
    """Test that registering with an existing username fails."""
    # Register first user
    with app.app_context():
        user = User(username='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    # Try to register with same username
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'password': 'TestPassword123',
        'password2': 'TestPassword123'
    }, follow_redirects=True)
    
    assert b'Username already taken' in response.data or b'already' in response.data


def test_login_page_loads(client):
    """Test that the login page loads successfully."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Welcome Back!' in response.data or b'Login' in response.data


def test_login_success(client, app):
    """Test successful login."""
    # Create a test user
    with app.app_context():
        user = User(username='testuser')
        user.set_password('TestPassword123')
        db.session.add(user)
        db.session.commit()
    
    # Login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'TestPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_login_invalid_username(client):
    """Test login with non-existent username."""
    response = client.post('/auth/login', data={
        'username': 'nonexistent',
        'password': 'password123'
    }, follow_redirects=True)
    
    # Check that we're still on the login page (login failed)
    assert response.status_code == 200
    assert b'Welcome Back!' in response.data or b'Login' in response.data

def test_login_invalid_password(client, app):
    """Test login with incorrect password."""
    # Create a test user
    with app.app_context():
        user = User(username='testuser')
        user.set_password('correctpassword')
        db.session.add(user)
        db.session.commit()
    
    # Try to login with wrong password
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    # Check that we're still on the login page (login failed)
    assert response.status_code == 200
    assert b'Welcome Back!' in response.data or b'Login' in response.data

    
def test_logout(client, app):
    """Test logout functionality."""
    # Create and login a user
    with app.app_context():
        user = User(username='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    })
    
    # Logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_password_hashing(app):
    """Test that passwords are properly hashed."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('mypassword')
        
        # Password should be hashed, not stored in plain text
        assert user.password_hash != 'mypassword'
        
        # Check password should work with correct password
        assert user.check_password('mypassword') is True
        
        # Check password should fail with incorrect password
        assert user.check_password('wrongpassword') is False
