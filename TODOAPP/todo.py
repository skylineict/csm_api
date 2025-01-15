from fastapi import APIRouter, HTTPException, Depends, Query,status
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
# from inventory.databaseconfi import engine, SessionDB, create_db_table
from databaseconfig import  engine, SessionDB, create_db_table
from securities import get_curent_user
from user_models import User

from model import TodoListResponse, TodoListSuccessResponse, createTodo, TodoList

router = APIRouter()


user_dependency = Annotated[User, Depends(get_curent_user)]




@router.post('/create',status_code=status.HTTP_201_CREATED, response_model=TodoListSuccessResponse)
async def creat_todo(user: user_dependency,todo:createTodo, session:SessionDB ):
    # new_todo =  TodoList(**todo.model_dump())
    new_todo = TodoList(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        created_by= user.id,
        complete=todo.complete

    )
    #save the data to database
    session.add(new_todo)
    session.commit()
    return {'success': 'to do created successfully',
            'datacreated': new_todo}



@router.get('/list',status_code=status.HTTP_202_ACCEPTED)
async def get_todo(session:SessionDB):
    todolist  = session.exec(select(TodoList)).all()

    return todolist





@router.get('/get_list{todo_id}', status_code=status.HTTP_200_OK )
async def get_all_todo(todo_id: int, db: SessionDB, user: user_dependency):
    todolist = db.exec(select(TodoList).where(TodoList.id==todo_id).where(TodoList.created_by==user.id)).first()
    if todolist is not None:
        return todolist
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Todo with the specified ID {todo_id} not found' )


@router.put('/updatelist{todo_id}', status_code=status.HTTP_200_OK,response_model=TodoListSuccessResponse)
async def update_todo(todo_id: int, db: SessionDB,todcreate: createTodo, user:user_dependency ):
    todolist = db.exec(select(TodoList).where(TodoList.id==todo_id).where(TodoList.created_by==user.id)).first()
    if todolist is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Todo with the specified ID {todo_id} not found' )
    todolist.title = todcreate.title
    todolist.description = todcreate.description
    todolist.priority = todcreate.priority
    todolist.complete =  todcreate.complete
    db.add(todolist)
    db.commit()
    return {'success': 'to do updated sucess',
            'datacreated': todolist}





   




