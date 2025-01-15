from fastapi import FastAPI
from databse import engine
from sqlmodel import Field,Session,SQLModel,create_engine,select
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
from pydantic import BaseModel,Field,HttpUrl,EmailStr



app = FastAPI()


class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, autoincrement=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), unique=True, index=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class DatabaseRes(BaseModel):
    name: str
    age: int | None = None
    secret_name: str

    class Config:
        orm_mode = True  



class HeroCreate(BaseModel):
    name: str
    age: int | None = None
    secret_name: str


# Session Dependency
def get_session():
    with Session(engine) as session:
        yield session


SessionDB = Annotated[Session, Depends(get_session)]

def create_db_table():
    SQLModel.metadata.create_all(engine)



# @app.on_event('startup')
# def on_startup():
#     create_db_table()


# app.include_router(students_endpoint, tags=['students endpoint'])

 


# @app.post('/create/', response_model=DatabaseRes)
# def create_hero(hero: HeroCreate, session: SessionDB) -> DatabaseRes:
#     db_here = Hero.model_validate(hero)
#     session.add(db_here)
#     session.commit()
#     session.refresh(db_here)
#     return db_here