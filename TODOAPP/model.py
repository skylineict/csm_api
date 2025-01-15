from sqlmodel import SQLModel,Field
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime



class TodoList(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: str  = Field(default=None, nullable=False)
    priority: int = Field(default=1, ge=1,le=5)
    complete: bool = Field(default=False)
    is_active: bool = Field(default=True)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    created_by : str = Field(foreign_key='user.id', nullable=False)

class createTodo(BaseModel):
    title : str = Field(min_length=3, max_length=200, description='Title must be between 3 and 100 characters')
    description: str = Field(min_length=5, description='Description must be at least 5 characters long')
    priority: int = Field(ge=1, le=5, description="Priority must be between 1 and 5.")
    complete: Optional[bool] = Field(default=False)


class TodoListResponse(BaseModel):
    id: int
    title: str 
    description: str 
    priority: int
    complete: bool 
    is_active: bool 
    date_created: datetime 
    class Config:
        orm_mode = True

 
class TodoListSuccessResponse(BaseModel):
    success: str
    datacreated: TodoListResponse

    