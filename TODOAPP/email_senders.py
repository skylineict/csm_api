import random
# import smtplib
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
  

def send_email_with_otp(email: str, otp: str):
    try:
        subject = "Your OTP Code"
        body = f"Hello,\n\nYour OTP code is: {otp}\n\nUse this code to verify your account."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, email, msg.as_string())

        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")




def send_email_with_resetpassword_otp(email: str, otp: str):
    try:
        subject = "OTP for Password Reset"
        body = f"Hello,\n\nYour OTP code is: {otp}\n\nUse this code to verify your account and create new password."
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, email, msg.as_string())

        print(f"OTP sent to {email}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP")
