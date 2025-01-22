import pytest
import os
import logging
from app import create_app, db
from models import User
from flask_bcrypt import Bcrypt
from flask_migrate import upgrade

bcrypt = Bcrypt()

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_app():
    """Fixture to configure the Flask app for testing with a separate database."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'  # Test-specific database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings
    bcrypt.init_app(app)  # Initialize bcrypt for testing

    logger.debug(f"Pytest Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Debug log

    with app.app_context():
        # Apply migrations for test database
        logger.debug("Applying migrations to test database...")
        upgrade()

        yield app

        # Cleanup after tests
        logger.debug("Cleaning up test database...")
        db.session.remove()
        db.drop_all()

        # Remove test database file
        if os.path.exists("test_users.db"):
            os.remove("test_users.db")
            logger.debug("Test database file removed.")

@pytest.fixture
def test_client(test_app):
    """Fixture to provide a test client for making HTTP requests."""
    return test_app.test_client()

@pytest.fixture
def create_test_user(test_app):
    """Fixture to create a test user in the isolated test database."""
    def _create_user(email, password, role='free'):
        with test_app.app_context():
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(email=email, password=hashed_password, role=role)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)  # Refresh to populate attributes like ID
            logger.debug(f"Created Test User: {user.email}, Role: {user.role}, ID: {user.id}")  # Debugging
            return user
    return _create_user

