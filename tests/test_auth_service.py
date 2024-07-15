import sys
import os
import sqlite3
from datetime import datetime, timedelta

# Add the parent directory to the sys.path
if '__file__' in globals():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

import pytest
from flask_app import create_app
from services.auth_service import init_db
from config import config

@pytest.fixture(scope='module', autouse=True)
def setup_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Initialize your database or other setup tasks
            init_db()
        yield client

@pytest.fixture(scope='module')
def register_user(setup_client):
    client = setup_client
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'message' in data

    # Retrieve the activation token from the database
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT token, expires_at FROM tokens WHERE token_type='activation'")
    token, expires_at = cursor.fetchone()
    conn.close()

    # Ensure the token is valid
    assert datetime.fromisoformat(expires_at) > datetime.now(), "Activation token has expired"

    return token

def test_activate(setup_client, register_user):
    client = setup_client
    token = register_user
    response = client.get(f'/activate/{token}')
    assert response.status_code == 200, f"Failed to activate with token: {response.data.decode('utf-8')}"
    data = response.get_json()
    assert 'message' in data

def test_login(setup_client, register_user):
    client = setup_client
    test_activate(client, register_user)  # Ensure the user is activated
    response = client.post('/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_forgot_password(setup_client):
    client = setup_client
    response = client.post('/forgot_password', json={
        "email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_remove_account(setup_client):
    client = setup_client
    response = client.post('/remove_account', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

if __name__ == "__main__":
    pytest.main()
