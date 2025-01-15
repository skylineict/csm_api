from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends,Request
from sqlmodel import select
from databaseconfig import SessionDB
from otpgen import otp_generator
import pytz
from typing import Annotated
from pydantic import BaseModel, EmailStr, HttpUrl
from social_auth.socials  import google_sso,facebook_sso
from social_auth.create_users_auth import create_or_update_user



local_time = pytz.timezone('Africa/Lagos')


router = APIRouter()


@router.get('/auth/google')
async def google_login():
       async with google_sso:
           return await google_sso.get_login_redirect()
   
@router.get("/auth/google/callback")
async def google_callback(request: Request, db: SessionDB):
     user_info = await google_sso.verify_and_process(request)
     print("this is the first",user_info)
     if not user_info:
        raise HTTPException(status_code=400, detail="Google authentication failed")
     user = create_or_update_user(db, user_info.email,'google',user_info.id, user_info.first_name, user_info.last_name )
     print("this is the second",user)
     return {"email": user_info.email, "id": user_info.id}




@router.get("/auth/facebook")
async def facebook_login():
    return await facebook_sso.get_login_redirect()

@router.get("/auth/facebook/callback")
async def facebook_callback(request: Request, db: SessionDB):
     user_info = facebook_sso.verify_and_process(request)
     print("this is the first",user_info)
     if not user_info:
        
        raise HTTPException(status_code=400, detail="facebook authentication failed")
     user = create_or_update_user(db, user_info.email,'google',user_info.id, user_info.first_name, user_info.last_name )
     print("this is the second",user)
     return {"email": user_info.email, "id": user_info.id}


     

