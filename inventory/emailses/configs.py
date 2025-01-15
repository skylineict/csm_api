import pyotp
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException


def otpgenerator():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.now()[:5] 





