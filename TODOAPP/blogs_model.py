from sqlmodel import SQLModel,Field
from pydantic import BaseModel, EmailStr, HttpUrl,field_validator
from typing import Optional,List
from datetime import datetime
import re
from user_models import User
import pytz
from fastapi import UploadFile
from sqlmodel import SQLModel, Field, Relationship

local_time = pytz.timezone('Africa/Lagos')


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, unique=True, nullable=False)
    description: Optional[str] = Field(default=None, max_length=500)
    posts: List["Post"] = Relationship(back_populates="category")

class PostTag(SQLModel, table=True):
    post_id: int = Field(foreign_key="post.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, nullable=False)
    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTag)

class PostImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id", nullable=False)
    image_url: str = Field(nullable=False)
    post: 'Post' = Relationship(back_populates="images")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    content: str = Field(nullable=False)
    image_url: Optional[str] = Field(default=None)
    author_id: int = Field(foreign_key="user.id", nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    is_approved: bool = Field(default=False)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    date_updated: datetime = Field(default_factory=datetime.utcnow)

    category: Category = Relationship(back_populates="posts")
    tags: List["Tag"] = Relationship(back_populates="posts", link_model=PostTag)
    comments: List["Comment"] = Relationship(back_populates="post")
    likes: List["PostLike"] = Relationship(back_populates="post")
    images: List["PostImage"] = Relationship(back_populates="post")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    content: str = Field(nullable=False, max_length=1000)
    date_created: datetime = Field(default_factory=datetime.utcnow)

    post: Post = Relationship(back_populates="comments")
    reactions: List["CommentReaction"] = Relationship(back_populates="comment")


class PostLike(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="post.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    date_created: datetime = Field(default_factory=datetime.utcnow)

    post: Post = Relationship(back_populates="likes")


class CommentReaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    comment_id: int = Field(foreign_key="comment.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    reaction: str = Field(max_length=50, nullable=False)  # e.g., "like", "love", "dislike"

    comment: Comment = Relationship(back_populates="reactions")


