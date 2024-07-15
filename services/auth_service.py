from flask import Blueprint, request, jsonify, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from config import config
from services.email_service import send_email

blueprint = Blueprint('auth', __name__)

DATABASE = config.DATABASE_PATH

def adapt_datetime(dt):
    return dt.isoformat()

def convert_datetime(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')  # Assuming UTF-8 encoding
    if s:
        return datetime.fromisoformat(s)
    return None

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter('timestamp', convert_datetime)

def get_db():
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return conn

def init_db():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 0,
                created_at timestamp NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS tokens (
                user_id TEXT NOT NULL,
                token TEXT NOT NULL,
                token_type TEXT NOT NULL,
                expires_at timestamp NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    print("Database initialized")

def generate_token(user_id, token_type):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=20)
    with get_db() as db:
        db.execute('''
            INSERT INTO tokens (user_id, token, token_type, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, token, token_type, expires_at))
    return token

@blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Invalid input'}), 400

    hashed_password = generate_password_hash(password)
    user_id = str(uuid.uuid4())
    created_at = datetime.now()

    with get_db() as db:
        db.execute('''
            INSERT INTO users (id, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, email, hashed_password, created_at))

    token = generate_token(user_id, 'activation')
    activation_link = url_for('auth.activate_account', token=token, _external=True)
    send_email([email], "Activate your account", f"Click here to activate: {activation_link}")

    return jsonify({'message': 'Check your email to activate your account'}), 201

@blueprint.route('/activate/<token>', methods=['GET'])
def activate_account(token):
    with get_db() as db:
        cur = db.execute('''
            SELECT user_id, expires_at FROM tokens
            WHERE token = ? AND token_type = 'activation'
        ''', (token,))
        token_data = cur.fetchone()

    if not token_data:
        return jsonify({'error': 'Invalid token'}), 400

    expires_at = token_data[1]

    if isinstance(expires_at, str):
        expires_at = convert_datetime(expires_at)  # Convert to datetime object

    if expires_at < datetime.now():
        return jsonify({'error': 'Token expired'}), 400

    user_id = token_data[0]

    with get_db() as db:
        db.execute('''
            UPDATE users SET is_active = 1 WHERE id = ?
        ''', (user_id,))
        db.execute('''
            DELETE FROM tokens WHERE token = ?
        ''', (token,))

    return jsonify({'message': 'Account activated'}), 200

@blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Invalid input'}), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT id, username, password, is_active FROM users WHERE email = ?
        ''', (email,))
        user = cur.fetchone()

    if not user or not check_password_hash(user[2], password) or not user[3]:
        return jsonify({'error': 'Invalid credentials'}), 400

    session['user_id'] = user[0]
    session['username'] = user[1]

    return jsonify({'message': 'Logged in'}), 200

@blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

@blueprint.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Invalid input'}), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT id FROM users WHERE email = ?
        ''', (email,))
        user = cur.fetchone()

    if user:
        token = generate_token(user[0], 'reset')
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        send_email([email], "Reset your password", f"Click here to reset: {reset_link}")

    return jsonify({'message': 'Check your email for a reset link'}), 200

@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return jsonify({'message': 'Provide a new password'})

    data = request.json
    new_password = data.get('password')

    if not new_password:
        return jsonify({'error': 'Invalid input'}), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT user_id, expires_at FROM tokens
            WHERE token = ? AND token_type = 'reset'
        ''', (token,))
        token_data = cur.fetchone()

    if not token_data or convert_datetime(token_data[1]) < datetime.now():
        return jsonify({'error': 'Invalid or expired token'}), 400

    user_id = token_data[0]
    hashed_password = generate_password_hash(new_password)

    with get_db() as db:
        db.execute('''
            UPDATE users SET password = ? WHERE id = ?
        ''', (hashed_password, user_id))
        db.execute('''
            DELETE FROM tokens WHERE token = ?
        ''', (token,))

    return jsonify({'message': 'Password reset successful'}), 200

@blueprint.route('/remove_account', methods=['POST'])
def remove_account():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Invalid input'}), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT id, password FROM users WHERE email = ?
        ''', (email,))
        user = cur.fetchone()

    if not user or not check_password_hash(user[1], password):
        return jsonify({'error': 'Invalid credentials'}), 400

    user_id = user[0]

    with get_db() as db:
        db.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        db.execute('''
            DELETE FROM tokens WHERE user_id = ?
        ''', (user_id,))

    return jsonify({'message': 'Account removed'}), 200
