
import pytest
from myapp import create_app
from myapp.database import db
import os
from environs import Env


env = Env()
env.read_env()
env_type = 'dev'

@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app(env_type)
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()

@pytest.fixture
def client(app):
    """Create database using Flask SQLAlchemy for the tests."""
    db.app = app
    with app.test_client() as client:
      with app.app_context():
        db.create_all()
      yield client
    # Explicitly close DB connection
    db.session.close()
    db.drop_all()
