import pytest
import tempfile
import os
from app import create_app
from app.extensions import db
from app.config.settings import TestingConfig

@pytest.fixture
def app():
    """Create application for testing."""
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['DATABASE_URL'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()

@pytest.fixture
def authenticated_client(client):
    """Authenticated test client."""
    client.post('/auth/login', data={
        'username': 'admin',
        'password': 'root'
    })
    return client