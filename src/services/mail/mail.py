import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
from env import config

def send_json_email(receiver_email, subject, body_content, attachment):
    sender_email = config["email"]["admin"]["email"]
    password = config["email"]["admin"]["password"]  

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body_content, "plain"))
    message.attach(attachment)
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
    except Exception as e:
        print(f"Lỗi gửi email: {e}")

def create_json_file(json_data, filename):  
    json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
    
    json_bytes = json_string.encode('utf-8')
    json_buffer = BytesIO(json_bytes)
    
    attachment = MIMEBase("application", "json")
    attachment.set_payload(json_buffer.getvalue())
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        "attachment",
        filename=filename
    )
    
    return attachment
