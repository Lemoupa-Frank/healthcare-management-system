import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from datetime import datetime, timedelta
from app.models import Appointment
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(to_email, subject, body):
    from_email = os.getenv('EMAIL_ADDRESS')
    from_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_sms(to_phone, body):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to=to_phone
    )

def send_reminders():
    now = datetime.now()
    reminder_time = now + timedelta(hours=24)  # Remind 24 hours before the appointment
    appointments = Appointment.find({'date_time': {'$lte': reminder_time}})

    for appointment in appointments:
        if appointment['reminder_method'] == 'email' and appointment['email']:
            send_email(appointment['email'], 'Appointment Reminder', 'Your appointment is scheduled for tomorrow.')
        elif appointment['reminder_method'] == 'sms' and appointment['phone']:
            send_sms(appointment['phone'], 'Your appointment is scheduled for tomorrow.')
