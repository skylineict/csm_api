from fastapi import APIRouter, HTTPException, Depends, Query,FastAPI
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from databaseconfi import engine, SessionDB, create_db_table
from sqlmodel import Field,Session,SQLModel,create_engine,select
from model import User
from routers import auth, sendemail_endpoint
app = FastAPI()






@app.on_event('startup')
def on_startup():
    create_db_table()


app.include_router(auth.router, tags=['register'])
app.include_router(sendemail_endpoint.router, tags=['send email'])