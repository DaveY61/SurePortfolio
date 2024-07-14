import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    LOG_FILE_DIRECTORY = os.environ.get('LOG_FILE_DIRECTORY') or 'logs'
    LOG_RETENTION_DAYS = int(os.environ.get('LOG_RETENTION_DAYS', 30))
    ENABLE_ERROR_EMAIL = os.environ.get('ENABLE_ERROR_EMAIL') == 'True'
    ADMIN_EMAILS = os.environ.get('ADMIN_EMAILS', '').split(',')

    # Email settings
    EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS')
    SMTP_SERVER = os.environ.get('SMTP_SERVER')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    EMAIL_QUEUE_DIRECTORY = os.environ.get('EMAIL_QUEUE_DIRECTORY') or 'email_queue'

config = Config()
