from user_models import User
from sqlmodel import select
from databaseconfig import SessionDB, get_session
from passlib.context import CryptContext
from datetime import timedelta,datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from collections import namedtuple
import jwt
import pytz
from user_models import User
import os
from dotenv import load_dotenv
from jwt.exceptions import ExpiredSignatureError

loca_timezone = pytz.timezone('Africa/Lagos')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()  # Load environment variables from the .env file

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def authenticate_user(username: str, password: str, db):
    user = db.exec(select(User).where(User.username==username)).first()
    if not user:
         return False
    if not pwd_context.verify(password, user.password):
         return False
    return user




def create_access_token(username: str, user_id: int, role: str, expired_date: timedelta):
     encoded = {
          'sub': username,
          'id': user_id,
          'role': role}
     expires =  datetime.now(loca_timezone) + expired_date
     print(f"this is my new time{expires}")
     encoded.update({'exp': expires})
     return jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_curent_user(session: SessionDB,token: str = Depends(oauth2_scheme)):
                    
     try:
          paylaod = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
          username = paylaod.get('sub')
          user_id = paylaod.get('id')
          role =   paylaod.get('role')
          if username is None or user_id is None:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user credentail')
          
          user = session.exec(select(User).where(User.id == user_id).where(User.role==role)).first()
          if user is None:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",)
          return user
        
         
          # return {'username': username, "user_id": user_id}
       
     except ExpiredSignatureError:
      
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
     except jwt.PyJWKError:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='could not validate user credentail')