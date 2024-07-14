import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.log_service import LogService

def test_log_service():
    # Define the log service
    log_service = LogService()

    # Create sample log entries (one for each type)
    log_service.log('INFO', 'This is an info message')
    log_service.log('WARNING', 'This is a warning message')
    log_service.log('ERROR', 'This is an error message')

    # Log entry with a "User ID"
    log_service.log('INFO', 'This message has a user id included', 'FRED')

    # Clean old logs
    log_service.clean_old_logs()

if __name__ == "__main__":
    test_log_service()
