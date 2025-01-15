from sqlmodel import Field,Session, SQLModel, create_engine,select
from pydantic import BaseModel, EmailStr, HttpUrl, validator
import uuid
from typing import Optional
from datetime import datetime


#alembic init migrations
#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), index=True, unique=True, nullable=False, max_length=200)
    email: EmailStr = Field(index=True, unique=True, nullable=False, max_length=200)
    full_name: str = Field(nullable=False)
    username: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    role: str = Field(default="staff", nullable=False)  # Can be "admin" or "staff"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


    
class UserCreate(BaseModel):
    email: EmailStr = Field(index=True, unique=True, nullable=False, max_length=200)
    full_name: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    username: str = Field(nullable=False)
    is_verified: bool = Field(default=False)
    role: str = Field(default="staff", nullable=False)  # Can be "admin" or "staff"
    



class UserResponse(BaseModel):
    uuid: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_uuid: str = Field(index=True, nullable=False, max_length=200)  # Foreign key relation to User UUID
    profile_picture: Optional[str] = Field(default=None)  # URL of the uploaded image
    address: Optional[str] = Field(default=None)
    gender: str = Field(nullable=False)  # Example: "Male", "Female", "Other"
    phone: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)




    


class UserProfileResponse(BaseModel):
    user_uuid: str
    profile_picture: Optional[HttpUrl]
    address: Optional[str]
    gender: str
    phone: Optional[str]
    bio: Optional[str]

    class Config:
        orm_mode = True



class OTPRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True, nullable=True, max_length=200)
    otp: str = Field(nullable=True)
    is_verified: bool = Field(default=False)
    date_created: datetime = Field(default_factory=datetime.utcnow)


class OTPRecordCreated(BaseModel):
    email : EmailStr

   

class ContactList(SQLModel, table=True):
    id: Optional[int] = Field(nullable=True, primary_key=True)
    phone:str = Field(nullable=True, max_length=20   0)