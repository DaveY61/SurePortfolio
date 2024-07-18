import sqlite3
import os
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime, timedelta
from config import config
from services.email_service import send_email

blueprint = Blueprint('auth', __name__, template_folder='auth_templates')

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

def init_db():
    if os.path.exists(DATABASE):
        print("Database already exists.")
        return

    print("Creating new database.")

    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    cursor = conn.cursor()

    # Create tables if they don't exist
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

def get_db():
    if not os.path.exists(DATABASE):
        print("Database does not exist. Initializing...")
        init_db()

    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
    return conn

def generate_token(user_id, token_type):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(minutes=20)
    with get_db() as db:
        db.execute('''
            INSERT INTO tokens (user_id, token, token_type, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, token, token_type, expires_at))
    return token

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # Otherwise handle the POST
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
    
    # Render the email template with the provided username and activation link
    email_body = render_template('activation_email.html', username=username, activation_link=activation_link)
    send_email([email], f"Activate your {config.APP_NAME} Account", email_body, html=True)

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
        return render_template('activation_failure.html'), 400

    expires_at = token_data['expires_at']

    if isinstance(expires_at, str):
        expires_at = convert_datetime(expires_at)  # Convert to datetime object

    if expires_at < datetime.now():
        return render_template('activation_failure.html'), 400

    user_id = token_data['user_id']

    with get_db() as db:
        db.execute('''
            UPDATE users SET is_active = 1 WHERE id = ?
        ''', (user_id,))
        db.execute('''
            DELETE FROM tokens WHERE token = ?
        ''', (token,))

    return render_template('activation_success.html'), 200

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    # Otherwise handle the POST
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return render_template('login_failure.html'), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT id, username, password, is_active FROM users WHERE email = ?
        ''', (email,))
        user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password) or not user['is_active']:
        return render_template('login_failure.html'), 400

    session['user_id'] = user['id']
    session['username'] = user['username']

    return redirect(url_for('home'))

@blueprint.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))

@blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    # Otherwise handle the POST
    data = request.form
    email = data.get('email')

    if not email:
        return render_template('invalid_input.html'), 400

    with get_db() as db:
        cur = db.execute('''
            SELECT id FROM users WHERE email = ?
        ''', (email,))
        user = cur.fetchone()

    if user:
        token = generate_token(user['id'], 'reset')
        reset_link = url_for('auth.reset_password', token=token, _external=True)

        # Render the email template with the provided username and reset link
        email_body = render_template('forgot_password_email.html', username=session['username'], activation_link=reset_link)
        send_email([email], f"Reset your {config.APP_NAME} Password", email_body, html=True)

    return render_template('forgot_password_response.html'), 200

@blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        return render_template('reset_password.html', token=token)

    # Otherwise handle the POST
    data = request.form
    new_password = data.get('password')

    if not new_password:
        return render_template('invalid_input.html'), 400
    
    with get_db() as db:
        cur = db.execute('''
            SELECT user_id, expires_at FROM tokens
            WHERE token = ? AND token_type = 'reset'
        ''', (token,))
        token_data = cur.fetchone()

    expires_at = token_data['expires_at']

    if isinstance(expires_at, str):
        expires_at = convert_datetime(expires_at)  # Convert to datetime object

    if expires_at < datetime.now():
        return render_template('invalid_input.html'), 400

    user_id = token_data['user_id']
    hashed_password = generate_password_hash(new_password)

    with get_db() as db:
        db.execute('''
            UPDATE users SET password = ? WHERE id = ?
        ''', (hashed_password, user_id))
        db.execute('''
            DELETE FROM tokens WHERE token = ?
        ''', (token,))

    session.clear()
    return render_template('reset_password_success.html'), 200

@blueprint.route('/remove_account', methods=['POST'])
def remove_account():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return render_template('invalid_input.html'), 400

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
