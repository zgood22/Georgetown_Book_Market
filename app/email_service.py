import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ENVIRONMENT VARIABLES AND CONSTANTS

load_dotenv() # go look in the .env file for any env vars

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")


def send_email(recipient_email, subject, message):
    # Ensure that you have set SENDGRID_API_KEY in your environment variables
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDGRID_API_KEY = "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"



    message = Mail(
        from_email='jlm456@georgetown.edu',
        to_emails=recipient_email,
        subject=subject,
        html_content=message
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("An error occurred:", e)

# Usage
if __name__ == "__main__":
    send_email('zig5@georgetown.edu', 'Test Subject', '<strong>Test message content</strong>')
