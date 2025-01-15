from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import datetime, timedelta
from passlib.context import CryptContext
from user_models import UserCreate, User, OtpRecords
from record_form import OtpCreate, Token,Change_password
from databaseconfig import SessionDB
from otpgen import otp_generator
from email_senders import send_email_with_otp, send_email_with_resetpassword_otp
import pytz
from securities import authenticate_user,create_access_token
from typing import Annotated
from pydantic import BaseModel, EmailStr, HttpUrl

local_time = pytz.timezone('Africa/Lagos')
def generate_unique_username(db: SessionDB, email: str):
    base_username = email.split('@')[0]
    username = base_username
    counter = 1

    while db.exec(select(User).where(User.username == username)).first():
        # If username exists, append a counter to it and try again
        username = f"{base_username}{counter}"
        counter += 1

    return username

def create_or_update_user(db: SessionDB, email: str, provider: str, provider_id: str,first_name: str, last_name: str):
   
   existing_user = db.exec(select(User).where(User.email == email)).first()
   if existing_user:
      if existing_user.oauth_provider == provider and existing_user.oauth_id == provider_id:
           return existing_user
      raise HTTPException(status_code=400, detail="Email already exists with a different OAuth provider")
   
   user = db.exec(select(User).where(User.oauth_provider == provider, User.oauth_id == provider_id)).first()
   if  user:
        return user
        
   username = generate_unique_username(db, email)

       
   first_name = first_name or "Unknown"
   last_name = last_name or "users"
   user = User(
            email=email,
            username=username,
            fist_name=first_name,
            last_name=last_name,
            password=None,  # No password needed for OAuth
            is_active=True,
            role='user',
            is_email_verifed=True,  # Assuming email is not verified at first
            date_created=datetime.now(local_time),
            oauth_provider=provider,
            oauth_id=provider_id
        )
   db.add(user)
   db.commit()
   db.refresh(user)  # Refresh the user object with the updated data
   return user
