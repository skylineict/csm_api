from model import Hero
from databse import get_session
from fastapi import APIRouter, HTTPException, Depends, Query
from model import HeroCreate, DatabaseRes
from typing import Annotated,Literal
from sqlmodel import Field,Session,SQLModel,create_engine,select
from .student_listendpoint import SessionDB

router = APIRouter()



@router.post('/create/', response_model=DatabaseRes)
def create_hero(hero: HeroCreate, session: SessionDB) -> DatabaseRes:
    db_here = Hero.model_validate(hero)
    session.add(db_here)
    session.commit()
    session.refresh(db_here)
    return db_here
   
    
    


# get all the students list
@router.get('/herelist/')
def heroList(
    session:SessionDB,
      offset: int= 0,
      limit: Annotated[int, Query(le=5)] = 5,) -> list[Hero]:
    hereolist = session.exec(select(Hero).offset(offset).limit(limit)).all()
    
    return hereolist



@router.delete('/here/{student_id}')
def delete_student(student_id: int, session: SessionDB):
    students = session.get(Hero, student_id)
    if not students:
          raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(students)
    session.commit()
    return {
        "success": "delete sucessfuly"
    }
