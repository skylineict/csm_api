from fastapi import APIRouter, HTTPException, Depends, Query,FastAPI
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime
from databaseconfig import create_db_table
from todo import router
from model import TodoList
from router import user_auth, admin,social_auth,porfiles_auth, follows,categories,blogs_cms,post_tags



# from databaseconfig  import create_db_table
app = FastAPI()



@app.on_event('startup')
def on_startup():
    create_db_table()



app.include_router(user_auth.router, tags=['User Auth'])
app.include_router(social_auth.router, tags=['social oauth '])
app.include_router(porfiles_auth.router, tags=['Profiles '])
app.include_router(blogs_cms.router, tags=['blog cms '])
app.include_router(follows.router, tags=['Follow Users '])
app.include_router(categories.router, tags=['Categories '])
app.include_router(post_tags.router, tags=['Post Tags Admin Endpoint '])
app.include_router(router, tags=['Todo List Crud'])



app.include_router(admin.router, tags=['Admin '])



# app.include_router(sendemail_endpoint.router, tags=['send email'])