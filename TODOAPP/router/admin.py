from fastapi import APIRouter,HTTPException,BackgroundTasks,status,Depends
from securities import get_curent_user
from user_models import User
from todo import user_dependency
from databaseconfig import  engine, SessionDB
from sqlmodel import select
from user_models import UserCreate,UserUpdate,Profile
from model import TodoList
from forms import Create_category
from blogs_model import Category



router = APIRouter()







router = APIRouter()  

@router.get('/user_todo',status_code=status.HTTP_202_ACCEPTED)

async def get_user_todo(session:SessionDB, user: user_dependency):
    if user is None or user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='permission decline')
    todolist  = session.exec(select(TodoList).where(TodoList.created_by==user.id)).all()

    return todolist


@router.put('/edit_user/{user_id}')
async def edit_user(user_id: int, session:SessionDB, user:user_dependency, userform:UserUpdate ):
    if user is None or user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='permission decline')
    edit_user = session.exec(select(User).where(User.id == user_id)).first()
    if edit_user is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Todo with the specified ID {user_id} not found' )
    
    edit_user.fist_name = userform.fist_name,
    edit_user.last_name = userform.last_name,
    edit_user.username = userform.username,
    edit_user.role = userform.role
    session.add(edit_user)
    session.commit()
    return {'success': 'user update suceessfull '}
    
    
@router.delete('/delete/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_and_profile(user_id: int, db: SessionDB, current_user: user_dependency):
    if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')

    # Retrieve the user to be deleted
    user_to_delete = db.exec(select(User).where(User.id == user_id)).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Retrieve and delete the profile associated with the user
    profile_to_delete = db.exec(select(Profile).where(Profile.user_id == user_to_delete.id)).first()
    
    if profile_to_delete:
        db.delete(profile_to_delete)
    
    # Delete the user
    db.delete(user_to_delete)
    
    db.commit()
    
    return {"message": f"User with ID {user_id} and their profile deleted successfully."}


@router.post('/category_create')
async def create_category( db: SessionDB, form:Create_category, current_user: user_dependency):
      if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
      category_exist = db.exec(select(Category).where(Category.name == form.name)).first()
      if category_exist:
           raise HTTPException(status_code=400, detail="category already exists")
      
      createcategory = Category(name=form.name,description=form.description)
      db.add(createcategory)
      db.commit()
      return {'success': 'category added sucessfully'}


@router.put('/category_edit{category_id}')
async def category_edit(category_id:int, db: SessionDB, form:Create_category, current_user: user_dependency):
      if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
      category = db.exec(select(Category).where(Category.id== category_id)).first()
      if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category with the specified ID {category_id} not found' )
      category.name = form.name,
      category.description = form.description
      db.add(category)
      db.commit()
      return {'success': 'category update sucessfully'}

@router.delete('/category_delete{category_id}')
async def category_delete(category_id:int, db: SessionDB, current_user: user_dependency):
      if current_user is None or current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permission denied')
      category = db.exec(select(Category).where(Category.id== category_id)).first()
      if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'category with the specified ID {category_id} not found' )
      db.delete(category)
      db.commit()
      return {'success': 'category delete sucessfully'}



    