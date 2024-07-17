import sqlite3
from flask import Blueprint, request, jsonify, session, render_template, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from config import config
from services.email_service import send_email

blueprint = Blueprint('auth', __name__, template_folder='templates')

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
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
    return conn

def init_db():
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 0,
            created_at timestamp NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            user_id TEXT NOT NULL,
            token TEXT NOT NULL,
            token_type TEXT NOT NULL,
            expires_at timestamp NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()
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

@blueprint.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

@blueprint.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return render_template('register_failure.html'), 400

    with get_db() as db:
        # Check if the email already exists
        cur = db.execute('SELECT id FROM users WHERE lower(email) = lower(?)', (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return render_template('register_failure.html'), 400

        hashed_password = generate_password_hash(password)
        user_id = str(uuid.uuid4())
        created_at = datetime.now()

        db.execute('''
            INSERT INTO users (id, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, email, hashed_password, created_at))

    token = generate_token(user_id, 'activation')
    activation_link = url_for('auth.activate_account', token=token, _external=True)
    send_email([email], "Activate your account", f"Click here to activate: {activation_link}")

    return render_template('register_success.html'), 201

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

    expires_at = token_data['expires_at']

    if isinstance(expires_at, str):
        expires_at = convert_datetime(expires_at)  # Convert to datetime object

    if expires_at < datetime.now():
        return jsonify({'error': 'Token expired'}), 400

    user_id = token_data['user_id']

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

    if not user or not check_password_hash(user['password'], password) or not user['is_active']:
        return jsonify({'error': 'Invalid credentials'}), 400

    session['user_id'] = user['id']
    session['username'] = user['username']

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
        token = generate_token(user['id'], 'reset')
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

    if not token_data or convert_datetime(token_data['expires_at']) < datetime.now():
        return jsonify({'error': 'Invalid or expired token'}), 400

    user_id = token_data['user_id']
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

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 400

    user_id = user['id']

    with get_db() as db:
        db.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        db.execute('''
            DELETE FROM tokens WHERE user_id = ?
        ''', (user_id,))

    return jsonify({'message': 'Account removed'}), 200
