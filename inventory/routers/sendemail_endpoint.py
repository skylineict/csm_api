from fastapi import APIRouter, HTTPException, Depends, Query,BackgroundTasks
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
from databaseconfi import engine, SessionDB, create_db_table
from model import User,OTPRecordCreated, OTPRecord
from datetime import datetime, timedelta
from emailses.configs  import otpgenerator
from emailses.emailsscript import send_email_with_otp


router = APIRouter()



   

@router.post('/send_otp/')
async def send_otp(request: OTPRecordCreated,  session:SessionDB, backgroundtask: BackgroundTasks):
    email_exist  = select(OTPRecord).where(OTPRecord.email == request.email)
    result = session.exec(email_exist).first()

    if result:
        if result.is_verified:
            raise HTTPException(status_code=400, detail="Email is already verified")
        
        if result.date_created + timedelta(minutes=3) > datetime.utcnow():
          raise HTTPException(
                status_code=400, 
                detail="OTP already sent. Please wait before requesting a new one."
            )
  
    otp = otpgenerator()
    if result:
        result.otp = otp
        result.date_created = datetime.utcnow()
        result.is_verified = False
        session.add(result)
    else:
        otp_created = OTPRecord(
            email = request.email,
            otp = otp,
            date_created = datetime.utcnow(),
            is_verified = False
        )

        session.add(otp_created)
        session.commit()
        backgroundtask(send_email_with_otp,request.email, otp)
        # send_email_with_otp(request.email, otp)
        return {"message": f"OTP sent to {request.email}"}





