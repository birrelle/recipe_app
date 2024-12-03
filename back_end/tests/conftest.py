import pytest
import os
from app import create_app
from flask import Flask
from app import database

# scope="session"
@pytest.fixture()
def app():
    test_app = create_app('testing')
    return test_app

@pytest.fixture(scope="function")
def client(app: Flask):
    """Create a test client for the Flask application"""
    with app.test_client() as test_client:
        # Establish application context
        with app.app_context():
            yield test_client

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_database():
    
    yield
    
    # Teardown: Runs after all tests are complete
    db = database.get_db()
    for collection_name in db.list_collection_names():
        db[collection_name].delete_many({})
