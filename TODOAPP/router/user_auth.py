from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import datetime, timedelta
from passlib.context import CryptContext
from user_models import UserCreate, User, OtpRecords,Profile
from record_form import OtpCreate, Token,Change_password
from databaseconfig import SessionDB
from otpgen import otp_generator
from email_senders import send_email_with_otp, send_email_with_resetpassword_otp
import pytz
from securities import authenticate_user,create_access_token
from typing import Annotated
from pydantic import BaseModel, EmailStr, HttpUrl



local_time = pytz.timezone('Africa/Lagos')
# get_utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
# mylocal_time_zone = get_utc_time.astimezone(local_time)

# print(mylocal_time_zone)



router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/create_user')
async def create_user(form:UserCreate, db:SessionDB, background: BackgroundTasks ):
    user_exist = db.exec(select(User).where(User.username == form.username)).first()
    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username already exist')
    
    email_exist = db.exec(select(User).where(User.email == form.email)).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email already already exist')
    
    passwordhashed = pwd_context.hash(form.password)

    created = User(
        username=form.username,
        last_name= form.last_name,
        first_name= form.first_name,
        email=form.email,
        password= passwordhashed)
    
    db.add(created)
    db.commit()
    otp = otp_generator()
    expired_at = datetime.now(local_time) + timedelta(minutes=3)
    # print(expired_at)
#create profile using the user creared instants
    profile = Profile(user_id=created.id)
    db.add(profile)
    db.commit()

    

  

    otp_records = OtpRecords (
    user_id=created.id,
    otp= otp,
    expiry_date= expired_at
    )
    db.add(otp_records)
    db.commit()

    background.add_task(send_email_with_otp, form.email, otp)

    # send_email_with_otp(form.email, otp)



    
    return {"message": "Account created successfully. OTP sent to your email"}




@router.post('/otp_verify')
async def otp_verify(otp:OtpCreate, db: SessionDB, background: BackgroundTasks ):
    otpselect = db.exec(select(OtpRecords).where(OtpRecords.otp == otp.otp)).first()
    user_id = db.exec(select(User).where(User.id == OtpRecords.user_id)).first()
  

    if not otpselect:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid OTP')
    mylocal_time_zone = datetime.now(local_time)

    otp_expiry_date = otpselect.expiry_date.astimezone(local_time)
    
    if otp_expiry_date < mylocal_time_zone:
        newotp = otp_generator()
        new_expired_date =  mylocal_time_zone + timedelta(minutes=20)
        otpselect.otp = newotp
        otpselect.is_verified = False
        otpselect.expiry_date = new_expired_date
        db.commit()
        background.add_task(send_email_with_otp, user_id.email, newotp)
        return {"message": "OTP expired. A new OTP has been sent to your email."}


    if user_id.is_email_verifed:
        return {"message": "Email aready verified"}

    otpselect.is_verified = True
    db.commit()

    
    user_id.is_email_verifed = True
    db.commit()
    return {"message": "Email verified successfully"}


form_datas = Annotated[OAuth2PasswordRequestForm,Depends()]

@router.post('/token',response_model=Token)
async def login_to_access_token(form_data: form_datas, db: SessionDB):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",)
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=3))
   
    return {
        'access_token': token, 'token_type': "bearer"
    }





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

revoked_token = set()
@router.post('/logout')
async def logout(token: str = Depends(oauth2_scheme)):
    revoked_token.add(token)
    return {"message": "Successfully logged out."}



@router.post('/forget-password')
async def forget_password(email: EmailStr, db:SessionDB, background: BackgroundTasks ):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email not found')
    otp = otp_generator()
    expiry_date = datetime.now(local_time) + timedelta(minutes=10)
    # otp_record = db.exec(select(OtpRecords).where(OtpRecords.user_id==user.id))

    # if otp_record:
    #     otp_record.otp = otp
    #     otp_record.expiry_date = expiry_date
    #     otp_record.is_verified = False
    #     db.commit()


    create_otp = OtpRecords(
        user_id= user.id,
        otp=otp,
        expiry_date=expiry_date,
        is_verified=False)
    
    db.add(create_otp)
    db.commit()
    background.add_task(send_email_with_resetpassword_otp, email, otp)

    return {"message": "A password reset OTP has been sent to your email."}




@router.post('/rest-password')
async def rest_password(new_password: Change_password, otp: str, comfirm_password, db: SessionDB):
    if new_password != comfirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='password not the same')
    
    otp_user = db.exec(select(OtpRecords).where(OtpRecords.otp==otp)).first()
    otp_expiry_date = otp_user.expiry_date.astimezone(local_time)
    if not otp_user or otp_expiry_date < datetime.now(local_time) or otp_user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP.")
    user  = db.exec(select(User).where(User.id ==otp_user.user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    user.password = pwd_context.hash(new_password)
    otp_user.is_verified = True
    db.commit()
    return {"message": "Password has been successfully reset."}



    
    