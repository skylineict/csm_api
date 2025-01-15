from sqlmodel import SQLModel,Field
from pydantic import BaseModel, EmailStr, HttpUrl,field_validator
from typing import Optional,List
from datetime import datetime
import re
import pytz
from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Relationship


local_time = pytz.timezone('Africa/Lagos')
# get_utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
# mylocal_time_zone = get_utc_time.astimezone(local_time)



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=5, index=True, max_length=200)
    email: EmailStr = Field(unique=True, min_length=5, index=True, max_length=200)
    first_name: Optional[str] = Field(default=None, max_length=200, index=True)
    last_name:Optional[str] = Field(default=None, max_length=200, index=True)
    password: Optional[str] = Field(default=None, max_length=200, index=True)
    is_active: bool = Field(default=True)
    role: str = Field(default='user')
    is_email_verifed: bool = Field(default=False)
    date_created: datetime = Field(default_factory=lambda: datetime.now(local_time))
    oauth_provider: Optional[str] = Field(default=None, nullable=True)  
    oauth_id: Optional[str] = Field(default=None, nullable=True)

class UserCreate(BaseModel):
    username: str
    email:   EmailStr
    first_name: str
    last_name: str
    password : str
    role: str = Field(default="user", description="Role of the user. Options: admin, staff, user.")
    
    @field_validator('password')
    def password_validator(value):

        if len(value) < 10:
            raise ValueError('Password must be at least 10 characters long')
        
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        return value

class UserUpdate(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str = Field(default="user", description="Role of the user. Options: admin, staff, user.")

    @field_validator('role')
    def role_validator(value):
        if value not in {"admin", "staff", "user"}:
            raise ValueError("Invalid role. Valid roles are: admin, staff, user.")
        return value





class OtpRecords(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key='user.id', nullable=False)
    otp: str = Field(nullable=False, max_length=5)
    is_verified: bool = Field(default=False)
    date_created: datetime =Field(default_factory=lambda:datetime.now(local_time))
    expiry_date: datetime = Field(nullable=False)




from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    bio: Optional[str] = Field(default=None, max_length=500)
    avatar_url: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None, max_length=200)
    date_created: datetime = Field(default_factory=datetime.utcnow)

    # Explicit foreign key specification to avoid ambiguity
    followers: List["UserFollower"] = Relationship(
        back_populates="followed",
        sa_relationship_kwargs={"foreign_keys": "UserFollower.followed_id"}
    )
    following: List["UserFollower"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "UserFollower.follower_id"}
    )


class CreateProfile(BaseModel):
    bio: str
    website:   HttpUrl
    avatar_url: UploadFile
    location: str
 
   
    
  




class UserFollower(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    follower_id: int = Field(foreign_key="profile.id")
    followed_id: int = Field(foreign_key="profile.id")
    date_created: datetime = Field(default_factory=datetime.utcnow)
    follower: "Profile" = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "UserFollower.follower_id"}
    )
    followed: "Profile" = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "UserFollower.followed_id"}
    )gi