from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends
from securities import get_curent_user
from user_models import User
from todo import user_dependency
from databaseconfig import  engine, SessionDB
from sqlmodel import select
from user_models import UserCreate,UserUpdate,Profile
from model import TodoList
from forms import Create_category
from blogs_model import Category, Post


router = APIRouter()


@router.get('/category_list')
async def category_list(db:SessionDB, user: user_dependency):
    categories = db.exec(select(Category)).all()
    return categories


@router.get('/categories{categorie_id}')
async def get_categories(categorie_id: int,db:SessionDB, user: user_dependency ):
    categories = db.exec(select(Category).where(Category.id ==categorie_id)).first()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category with id not found")
    return categories

@router.get('/post_category/{category_id}')
async def post_categories(categorie_id: int,db:SessionDB, user: user_dependency):
    category = db.exec(select(Category).where(Category.id==categorie_id)).first()
    if not category:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="category with id not found")
    post = db.exec(select(Post).where(Post.category_id==categorie_id, Post.author_id==user.id)).all()
    if not post:
        raise HTTPException(status_code=404, detail="No posts found in this category")

    return post
