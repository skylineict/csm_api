from sqlmodel import create_engine
from fastapi import APIRouter, HTTPException, Depends, Query,FastAPI
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select
from model import User

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = int(os.getenv("MYSQL_PORT"))
mysql_db = os.getenv("MYSQL_DB")

mysql_url = f"mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
engine = create_engine(mysql_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
def create_db_table():
    SQLModel.metadata.create_all(engine)

SessionDB = Annotated[Session, Depends(get_session)]

