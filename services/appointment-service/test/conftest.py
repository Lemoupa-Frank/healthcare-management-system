import sys
import os
import pytest

# Ensure the app directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.models import get_db, Appointment

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/appointment_service_test",
    })

    with app.app_context():
        # Initialize the database
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def run_around_tests(app):
    with app.app_context():
        db = get_db()
        # Clear the appointments collection before each test
        db.appointments.delete_many({})
        yield
        # Code to run after each test
