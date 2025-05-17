import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
gmail_address = os.getenv('GMAIL_EMAIL')
app_password = os.getenv('APP_PASSWORD')
to_number = os.getenv('ATT_PHONE_NUMBER')
to_email = os.getenv('YAHOO_EMAIL')
message_text = 'Hello from Python via Gmail!'

# --- EMAIL SETUP ---
msg = EmailMessage()
msg.set_content(message_text)
msg['From'] = gmail_address
msg['To'] = to_email
msg['Subject'] = 'Personal Alert Assistant(PAA)'

# --- SEND EMAIL ---
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(gmail_address, app_password)
    smtp.send_message(msg)

print("Email sent!")