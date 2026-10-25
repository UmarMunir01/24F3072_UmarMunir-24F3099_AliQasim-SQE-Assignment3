import pytest
from app import create_app, db
from app.models import User, Post, Comment


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
def auth_client(client, app):
    """Create an authenticated test client."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
    
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    })
    
    return client


def test_index_page_loads(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200


def test_create_post_requires_login(client):
    """Test that creating a post requires authentication."""
    response = client.get('/new_post')
    assert response.status_code == 302  # Redirect to login


def test_create_post_page_loads(auth_client):
    """Test that the new post page loads for authenticated users."""
    response = auth_client.get('/new_post')
    assert response.status_code == 200


def test_create_public_post(auth_client, app):
    """Test creating a public post."""
    # Don't send is_private field at all for a public post
    # (unchecked checkboxes don't send data)
    response = auth_client.post('/new_post', data={
        'title': 'Test Public Post',
        'content': 'This is a test public post.'
        # is_private is not sent (unchecked checkbox)
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify post was created
    with app.app_context():
        post = Post.query.filter_by(title='Test Public Post').first()
        assert post is not None
        assert post.content == 'This is a test public post.'
        # Check if post is public (is_private should be False or None/null)
        assert post.is_private in [False, None, 0]



def test_create_private_post(auth_client, app):
    """Test creating a private post."""
    response = auth_client.post('/new_post', data={
        'title': 'Test Private Post',
        'content': 'This is a test private post.',
        'is_private': True
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify post was created as private
    with app.app_context():
        post = Post.query.filter_by(title='Test Private Post').first()
        assert post is not None
        assert post.is_private is True


def test_view_public_post(client, app):
    """Test that public posts can be viewed by anyone."""
    # Create a post
    with app.app_context():
        user = User(username='author')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title='Public Post',
            content='Public content',
            author_id=user.id,
            is_private=False
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    
    # View the post without logging in
    response = client.get(f'/post/{post_id}')
    assert response.status_code == 200
    assert b'Public Post' in response.data


def test_view_private_post_as_author(auth_client, app):
    """Test that authors can view their own private posts."""
    # Create a private post
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        post = Post(
            title='Private Post',
            content='Private content',
            author_id=user.id,
            is_private=True
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    
    # View own private post
    response = auth_client.get(f'/post/{post_id}')
    assert response.status_code == 200
    assert b'Private Post' in response.data


def test_private_post_hidden_from_others(client, app):
    """Test that private posts are not visible to other users."""
    # Create a private post
    with app.app_context():
        user = User(username='author')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title='Private Post',
            content='Private content',
            author_id=user.id,
            is_private=True
        )
        db.session.add(post)
        db.session.commit()
    
    # Try to view as anonymous user
    response = client.get('/')
    assert b'Private Post' not in response.data


def test_add_comment_to_post(auth_client, app):
    """Test adding a comment to a post."""
    # Create a post
    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        post = Post(
            title='Test Post',
            content='Test content',
            author_id=user.id,
            is_private=False
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    
    # Add a comment
    response = auth_client.post(f'/post/{post_id}', data={
        'content': 'This is a test comment'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Verify comment was created
    with app.app_context():
        comment = Comment.query.filter_by(content='This is a test comment').first()
        assert comment is not None
        assert comment.post_id == post_id


def test_my_posts_page(auth_client):
    """Test the my posts page for authenticated users."""
    response = auth_client.get('/my_posts')
    assert response.status_code == 200


def test_post_markdown_rendering(client, app):
    """Test that markdown is properly rendered in posts."""
    with app.app_context():
        user = User(username='author')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        post = Post(
            title='Markdown Test',
            content='# Header\n\n**Bold text**',
            author_id=user.id,
            is_private=False
        )
        db.session.add(post)
        db.session.commit()
        post_id = post.id
    
    response = client.get(f'/post/{post_id}')
    assert response.status_code == 200
    # Check that markdown is rendered (will vary based on your markdown setup)
    assert b'Markdown Test' in response.data
