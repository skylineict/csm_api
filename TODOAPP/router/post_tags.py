
from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends,Form
from securities import get_curent_user
from user_models import User
from todo import user_dependency
from databaseconfig import  engine, SessionDB
from sqlmodel import select
from user_models import UserCreate,UserUpdate,Profile
from model import TodoList
from forms import Create_category
from blogs_model import Category,Tag
from typing import Annotated, List


router = APIRouter()


@router.post('/create_tag')
async def create_tag( db: SessionDB, name:Annotated[str, Form()], current_user: user_dependency):
      if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
      tag_exist = db.exec(select(Tag).where(Tag.name == name)).first()
      if tag_exist:
           raise HTTPException(status_code=400, detail="tag already exists")
      
      
      tag = Tag(name=name)
      db.add(tag)
      db.commit()
      return {'success': 'category added sucessfully'}


@router.get('/tags', response_model=List[Tag])
async def list_tags(db: SessionDB,current_user: user_dependency):
    tags = db.exec(select(Tag)).all()
    return tags
