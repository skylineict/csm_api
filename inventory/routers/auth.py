
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
from databaseconfi import engine, SessionDB, create_db_table
from model import User

router = APIRouter()

@router.post('/create_user')
async def create(user: User, session: SessionDB ) -> User:
    session.add(user)
    session.commit()
    # session.refresh(user)
    return user

