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
