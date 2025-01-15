from sqlmodel import SQLModel
import uuid
from pydantic import BaseModel,Field,HttpUrl,EmailStr

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


# create immigration files
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
# alembic revision --autogenerate -m "Add new table"

