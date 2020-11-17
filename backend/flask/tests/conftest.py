
import pytest
from myapp import create_app
from myapp.database import db
from myapp.sqlite3_db import init_app, close_db


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app()
    ctx = _app.test_request_context()
    ctx.push()
    yield _app
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


@pytest.fixture
def client2():
    """Create database using sqlite3.py and squema.sql files for the tests."""
    app = create_app()
    with app.test_client() as client:
      with app.app_context():
        init_app(app)        
      yield client    
    # Explicitly close DB connection
    
  