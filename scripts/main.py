import smtplib
import os
import weather_app_info

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Configurations
gmail_address = os.getenv('GMAIL_EMAIL')
app_password = os.getenv('APP_PASSWORD')
to_number = os.getenv('ATT_PHONE_NUMBER')
to_email = os.getenv('YAHOO_EMAIL')
weather = weather_app_info.WeatherAppInfo().organize_weather_data()
message_text = weather

# Email Setup
msg = EmailMessage()
msg.set_content(message_text)
msg['From'] = gmail_address
msg['To'] = to_email
msg['Subject'] = 'Personal Alert Assistant(PAA)'

# Send Email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(gmail_address, app_password)
    smtp.send_message(msg)
