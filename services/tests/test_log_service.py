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
