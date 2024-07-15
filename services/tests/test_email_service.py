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
from services.email_service import send_email,check_and_resend_failed_emails

def test_email_service():
    send_email(
        to=["test@example.com"],
        subject="Test Email",
        body="This is a test email.",
        html=None,
        attachments=[],
        cc=[],
        bcc=[]
    )
    check_and_resend_failed_emails()

if __name__ == "__main__":
    test_email_service()
