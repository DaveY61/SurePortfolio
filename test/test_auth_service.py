from flask import Flask
from services.auth_service import blueprint as auth_blueprint

def test_auth_service():
    app = Flask(__name__)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # Test the endpoints
    with app.test_client() as client:
        # Test login
        response = client.post('/auth/login', json={'username_or_email': 'user', 'password': 'pass'})
        print('Login:', response.json)

        # Test register
        response = client.post('/auth/register', json={'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass'})
        print('Register:', response.json)

if __name__ == "__main__":
    test_auth_service()
