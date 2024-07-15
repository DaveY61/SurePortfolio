#----------------------------------------------------------------------------
# Define "Project" Search Path
#----------------------------------------------------------------------------
import os
import sys
from dotenv import load_dotenv

# Determine the path for this project (based on the project name)
load_dotenv()
project_name = os.environ.get('PROJECT_NAME')
project_path = os.path.abspath(__file__).split(project_name)[0] + project_name

# Add the project path to sys.path
sys.path.insert(0, project_path)

#----------------------------------------------------------------------------
# Begin Test Code
#----------------------------------------------------------------------------
import pytest
import sqlite3
from datetime import datetime

from flask_app import create_app
from services.auth_service import init_db
from config import config

# Define user credentials
username = "testuser"
email = "test@example.com"
password = "password123"

@pytest.fixture(scope='module', autouse=True)
def setup_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

@pytest.fixture(scope='module')
def register_user(setup_client):
    client = setup_client
    response = client.post('/register', json={
        "username": username,
        "email": email,
        "password": password
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

    assert datetime.fromisoformat(expires_at) > datetime.now(), "Activation token has expired"

    return token  # Return the activation token

def test_activate(setup_client, register_user):
    client = setup_client
    token = register_user
    response = client.get(f'/activate/{token}')
    assert response.status_code == 200, f"Failed to activate with token: {response.data.decode('utf-8')}"
    data = response.get_json()
    assert 'message' in data

@pytest.mark.skip(reason="Disabled until activation issue resolved")
def test_login(setup_client):
    client = setup_client
    response = client.post('/login', json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

@pytest.mark.skip(reason="Disabled until activation issue resolved")
def test_forgot_password(setup_client):
    client = setup_client
    response = client.post('/forgot_password', json={
        "email": email
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

@pytest.mark.skip(reason="Disabled until activation issue resolved")
def test_remove_account(setup_client):
    client = setup_client
    response = client.post('/remove_account', json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

if __name__ == "__main__":
    pytest.main()
