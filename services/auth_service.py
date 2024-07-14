from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
from config import config  # Use relative import

blueprint = Blueprint('auth_service', __name__)

users = {}
key_to_user = {}
key_expiry = {}

# Helper function to generate a unique key
def generate_key():
    return str(uuid.uuid4())

# Helper function to validate keys
def valid_key(key):
    if key in key_to_user and key in key_expiry:
        if datetime.now() < key_expiry[key]:
            return True
    return False

@blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    user = users.get(username_or_email)
    if user and check_password_hash(user['password'], password):
        session['user'] = user
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 400

@blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logout successful"}), 200

@blueprint.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    if email in users:
        key = generate_key()
        key_to_user[key] = email
        key_expiry[key] = datetime.now() + timedelta(minutes=20)
        # send reset link logic here, including key
        return jsonify({"message": "Check your email for the reset link"}), 200
    return jsonify({"error": "Email not found"}), 400

@blueprint.route('/reset_password', methods=['POST'])
def reset_password():
    key = request.json.get('key')
    new_password = request.json.get('new_password')
    if valid_key(key):
        email = key_to_user.pop(key)
        key_expiry.pop(key)
        user = users.get(email)
        user['password'] = generate_password_hash(new_password)
        return jsonify({"message": "Password reset successful"}), 200
    return jsonify({"error": "Invalid or expired key"}), 400

@blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = generate_password_hash(data.get('password'))
    if email in users:
        return jsonify({"error": "Email already registered"}), 400
    users[email] = {"username": username, "email": email, "password": password}
    key = generate_key()
    key_to_user[key] = email
    key_expiry[key] = datetime.now() + timedelta(minutes=20)
    # send activation link logic here, including key
    return jsonify({"message": "Check your email to activate your account"}), 200

@blueprint.route('/activate_account', methods=['POST'])
def activate_account():
    key = request.json.get('key')
    if valid_key(key):
        email = key_to_user.pop(key)
        key_expiry.pop(key)
        # add user activation logic here
        return jsonify({"message": "Account activated successfully"}), 200
    return jsonify({"error": "Invalid or expired key"}), 400

@blueprint.route('/remove_account', methods=['POST'])
def remove_account():
    data = request.json
    username_or_email = data.get('username_or_email')
    password = data.get('password')
    user = users.get(username_or_email)
    if user and check_password_hash(user['password'], password):
        # remove user logic here
        return jsonify({"message": "Account removed successfully"}), 200
    return jsonify({"error": "Invalid credentials"}), 400
