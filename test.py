#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client


class SendEmails:
    def __init__(self, credentials: dict):
        self.sender_email = credentials.get("email")
        self.password = credentials.get("password")  # Use the generated App Password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587

    def send_email(self, receiver_email: str, subject: str = "Test Email", body: str = "Hello, this is a test email!"):
        try:
            # Create email message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()  # Secure the connection
            server.login(self.sender_email, self.password)  # Use App Password

            # Send email
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            server.quit()

            return f"True, email sent to {receiver_email}"
        except Exception as e:
            return f"False, Error: {str(e)}"

class SendSMS:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def send_sms(self, receiver_number, message):
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.twilio_number,
                to=receiver_number
            )
            return True, f"SMS sent to {receiver_number} (SID: {msg.sid})"
        except Exception as e:
            return False, f"Error: {str(e)}"

# Example usage
# sms_sender = SendSMS("your_account_sid", "your_auth_token", "+1234567890")
# print(sms_sender.send_sms("+9876543210", "Hello, this is a test SMS!"))

# Example Usage:
if __name__ == "__main__":
    credentials = {"email": "coolkatsumi@gmail.com", "password": "katsusun_PWD"}
    send_emails = SendEmails(credentials)
    response = send_emails.send_email("sirmohamedh@gmail.com")
    print(response)
