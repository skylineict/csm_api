from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from model import Hero
from databse import get_session
from sqlmodel import Field,Session,SQLModel,create_engine,select


SessionDB = Annotated[Session, Depends(get_session)]

router = APIRouter()


@router.get('/student_lists/')
def students_list(identifier: str, session: SessionDB) -> Hero:
    if identifier.isdigit():
        students = session.get(Hero, int(identifier))
    else:
        students  = session.exec(select(Hero).where(Hero.uuid==identifier)).first()
        if not students:
             students  = session.exec(select(Hero).where(Hero.name==identifier)).first()

        if not students:
             students  = session.exec(select(Hero).where(Hero.age==identifier)).first()
            
    if not students:
         raise HTTPException(status_code=404, detail="Student not found")
    
    return students



