from sqlmodel import create_engine
from fastapi import APIRouter, HTTPException, Depends, Query,FastAPI
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel import Field,Session,SQLModel,create_engine,select

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

mysql_username = os.getenv("MYSQL_USERNAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = int(os.getenv("MYSQL_PORT"))
mysql_db = os.getenv("MYSQL_DB")

DATABASE_URL = "mysql+pymysql://todolist:todolist@localhost:3306/todolist"
# This creates an engine instance to interact with the database. 
engine = create_engine(DATABASE_URL, echo=True)

# This function 'get_session' is a dependency that will provide a database session whenever it's called.
# The 'Session' object is used to interact with the database, to perform queries, or crud
def get_session():
    with Session(engine) as session:
        yield session

# This function 'create_db_table' is responsible for creating tables in the database
# based on the defined SQLModel classes (models)
def create_db_table():
    SQLModel.metadata.create_all(engine)

# So, in this case, 'SessionDB' will give FastAPI a database session for any endpoint that requires it.
# When this dependency is used in an endpoint, FastAPI will automatically call `get_session()` and provide the session object to the endpoint.
SessionDB = Annotated[Session, Depends(get_session)]





