from fastapi import APIRouter, HTTPException, Depends, Query,status,Form,UploadFile
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
# from inventory.databaseconfi import engine, SessionDB, create_db_table
from databaseconfig import  engine, SessionDB, create_db_table
from securities import get_curent_user
from user_models import User,Profile, CreateProfile,UserFollower
from datetime import datetime, timedelta
from pydantic import HttpUrl
from forms import FollowRequest

import pytz
router = APIRouter()
user_dependency = Annotated[User, Depends(get_curent_user)]


local_time = pytz.timezone('Africa/Lagos')


@router.post('/follow')
async def follows(user: user_dependency, id: FollowRequest,db: SessionDB ):
    checking_profile = db.exec(select(Profile).where(Profile.id == id.followed_id)).first()
    
    if not checking_profile:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The profile you are trying to follow does not exist"
        )
    
    existing_followers = db.exec(select(UserFollower).where(UserFollower.follower_id==user.id, UserFollower.followed_id==id.followed_id)).first()


    if existing_followers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this profile"
        )
    
    follow = UserFollower(
    follower_id=user.id,
    followed_id=id.followed_id)   
    
    db.add(follow)
    db.commit()
    return {"message": "Successfully followed the profile"}

 


@router.delete('/unfollow{followed_id}')
async def unfollows(user: user_dependency, followed_id:int, db: SessionDB ):
 
    
    follow = db.exec(select(UserFollower).where(UserFollower.follower_id==user.id, UserFollower.followed_id==followed_id)).first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="followe not found"
        )
    
    db.delete(follow)
    db.commit()
    return {"message": "Successfully unfollowed the profile"}

 
@router.get('/followers', status_code=status.HTTP_202_ACCEPTED)
async def get_followers(session: SessionDB, user: user_dependency):
    follower_ids = session.exec(
        select(UserFollower.follower_id)
        .where(UserFollower.followed_id == user.id)
    ).all()

    if not follower_ids:
        return{
            'messaage': 'No followers found'
        }
    # followers = session.exec(
    #     select(Profile)
    #     .where(Profile.id.in_(follower_ids))
    # ).all()

    return follower_ids


@router.get('/following')
async def get_following(session: SessionDB, user: user_dependency):
     following = session.exec(
        select(UserFollower.followed_id).where(UserFollower.follower_id == user.id)
    ).all()
     
    
     
     return {"following": following}
