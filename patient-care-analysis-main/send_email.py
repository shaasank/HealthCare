import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv
from email.mime.text import MIMEText
import time 
import streamlit as st

# Load environment variables
current_dir = Path.cwd()
env_vars = current_dir / ".env"
load_dotenv(env_vars)

sender_email = st.secrets["EMAIL"]
password =st.secrets["PASSWORD"]

if not sender_email or not password:
    raise ValueError("Email or password environment variables are not set")
def list_to_html(items,ch):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items.split(ch)) + "</ul>"
def send_email(user_record):
        # Create the email message
    
    try:
        msg = EmailMessage()
        msg['Subject'] = "Health Report"
        msg['From'] = formataddr(("Health Partner", sender_email))
        msg['To'] = user_record.get('email')
        # Set email content
        dis=user_record['extra_diseases'].split(',')
        html_content = f"""\
        <html>
            <body>
            <h1>Health Report</h1>
            <h4>Dear {user_record.get('name', 'User')},</h4>
            <p>I hope you are well. I just wanted to drop a quick note to remind you.</p>
            <img src="https://img.freepik.com/free-photo/top-view-world-heart-day-concept-with-stethoscope_23-2148631003.jpg?t=st=1723480589~exp=1723484189~hmac=cebd23933b00063c372c7c66a12a58bba964f133360eded7fad6c1519f302cd0&w=740">
            <p>Our team thinks, You might have been affected with  <strong>{user_record.get('disease', 'N/A')} disease</strong> </p>
            <p>Description of the disease: <strong>{user_record.get('description', 'N/A')}</strong></p>
            <strong>Are you following these</strong>
            <p>Precautions: {user_record.get('precautions', 'N/A')}</p>
            <p>Medications: {user_record.get('medications', 'N/A')}</p>
            <p>Diet: {list_to_html(user_record.get('diet', 'N/A'),' ')}</p>
            <p>Do's & Dont's: {user_record.get('workout', 'N/A')}</p>
            <p>Personalized Advice: {list_to_html(user_record.get('Personalized Advice', 'N/A'),'\n')}</p>
            <ul>You might also have these diseases:
             <li>{dis[0]}</li>
             <li>{dis[1]}</li>
             </ul>
             <p>Best regards,<br>Your Health Partner</p>

        </body>
     </html>
    """
        msg.set_content("This email requires an HTML-compatible email client.")
        msg.add_alternative(html_content, subtype='html')
        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            print(user_record,'bbkjb')
            server.login(sender_email, password)
            server.sendmail(sender_email,user_record.get('email'),msg.as_string())
            
        print(f"Email sent to {user_record.get('email')}")
        

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# For testing purposes, you can uncomment and run this code snippet
# if __name__ == "__main__":
#     send_email({
#         "email": "john.doe@example.com",
#         "name": "John Doe",
#         "disease": "fever",
#         "description": "xyz",
#         "precautions": "don't go out",
#         "medications": "paracetamol",
#         "diet": "rice",
#         "workout": "jogging",
#         "Personalized Advice": "Stay hydrated"
#     })
