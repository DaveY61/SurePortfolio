import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask_app import create_app
from services.auth_service import init_db
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Initialize your database or other setup tasks
            init_db()
        yield client

def test_register(client):
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data

def test_login(client):
    response = client.post('/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_forgot_password(client):
    response = client.post('/forgot_password', json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_remove_account(client):
    response = client.post('/remove_account', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

if __name__ == "__main__":
    pytest.main()
