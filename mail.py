import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv

def send_email(product_name, price, target_price):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = f"The price has dropped: {product_name}"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content(
        f"The price of {product_name} has dropped!"
        f"Current price: £{price}"
        f"Target price: £{target_price}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)