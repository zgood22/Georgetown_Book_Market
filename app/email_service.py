import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ENVIRONMENT VARIABLES AND CONSTANTS

load_dotenv() # go look in the .env file for any env vars

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def send_email(recipient_email, subject, message):
    # Ensure that you have set SENDGRID_API_KEY in your environment variables
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')

    if not sendgrid_api_key:
        raise ValueError("SendGrid API Key not found in environment variables")

    message = Mail(
        from_email='jlm456@georgetown.edu',  # Replace with your SendGrid verified sender email
        to_emails=recipient_email,
        subject=subject,
        html_content=message
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("An error occurred:", e)

# Usage
if __name__ == "__main__":
    send_email('zig5@georgetown.edu', 'Test Subject', '<strong>Test message content</strong>')
