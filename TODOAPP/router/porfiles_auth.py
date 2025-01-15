from fastapi import APIRouter, HTTPException, Depends, Query,status,Form,UploadFile
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
# from inventory.databaseconfi import engine, SessionDB, create_db_table
from databaseconfig import  engine, SessionDB, create_db_table
from securities import get_curent_user
from user_models import User,Profile, CreateProfile
from datetime import datetime, timedelta
from pydantic import HttpUrl

import pytz

local_time = pytz.timezone('Africa/Lagos')

from model import TodoListResponse, TodoListSuccessResponse, createTodo, TodoList

router = APIRouter()


user_dependency = Annotated[User, Depends(get_curent_user)]


@router.put('/profile',status_code=status.HTTP_201_CREATED)
async def create_profiles(user: user_dependency,bio: Annotated[str, Form()],
                          website: Annotated[HttpUrl, Form()],
                          location: Annotated[str, Form()],
                          avatar: UploadFile,db:SessionDB ):

        profile = db.exec(select(Profile).where(Profile.user_id== user.id)).first()
        if not profile:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        
        avatar_path = f"uploads/avatars/{avatar.filename}"
        with open(avatar_path, "wb") as buffer:
              buffer.write(await avatar.read())
     
        profile.bio = bio
        profile.website = website
        profile.location = location
        profile.avatar_url = avatar_path
        profile.date_created = datetime.now(local_time)
        db.add(profile)
        db.commit()
        return {'success': 'Create profile successfully',}



@router.get('/get_profile')
async def get_profile(user:user_dependency,db:SessionDB):
         # Retrieve the profile of the current user
        profile = db.exec(select(Profile).where(Profile.user_id== user.id)).first()
        if not profile:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
        return {
        "bio": profile.bio,
        "website": profile.website,
        "location": profile.location,
        "avatar_url": profile.avatar_url,
        "date_created": profile.date_created
    }
        

@router.post('/profile/avatar', status_code=status.HTTP_200_OK)
async def upload_avatar(user: user_dependency, avatar: UploadFile, db: SessionDB):
    # Retrieve the profile of the current user
    profile = db.exec(select(Profile).where(Profile.user_id == user.id)).first()
    
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    
    # Save the new avatar file
    avatar_path = f"uploads/avatars/{avatar.filename}"
    with open(avatar_path, "wb") as buffer:
        buffer.write(await avatar.read())
    
    # Update the avatar URL in the profile
    profile.avatar_url = avatar_path
    db.add(profile)
    db.commit()
    
    return {"success": "Avatar updated successfully", "avatar_url": avatar_path}
