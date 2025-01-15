from fastapi import APIRouter, HTTPException, Depends, Query,status,Form,UploadFile
from sqlmodel import select
from typing import Annotated, List
from sqlmodel import Session
# from inventory.databaseconfi import engine, SessionDB, create_db_table
from databaseconfig import  engine, SessionDB, create_db_table
from securities import get_curent_user
from user_models import User
from datetime import datetime, timedelta
from pydantic import HttpUrl
from blogs_model import Post,PostImage, PostTag,Tag,Category
import os

#  category = session.exec(select(Category).where(Category.id == category_id)).first()
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")

import pytz
user_dependency = Annotated[User, Depends(get_curent_user)]
local_time = pytz.timezone('Africa/Lagos')

router = APIRouter()

@router.post('/post')
async def create_post(
    user: user_dependency, 
    db: SessionDB,
    title: Annotated[str, Form()],
    content: Annotated[str, Form()],
    category_id: Annotated[int, Form()],
    image_url: UploadFile,
    additional_images: List[UploadFile],
    tags: Annotated[List[str], Form()]  # Tags are still passed as a List[str]
):
  
    # Validate category
    category = db.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if all the tags exist in the database
    # existing_tags = db.exec(select(Tag).where(Tag.id.in_(tags))).all()
    # existing_tag_ids = [tag.id for tag in existing_tags]

    # If the number of existing tags does not match the number of tags provided, raise an error
    # if len(existing_tag_ids) != len(tags):
    #     raise HTTPException(status_code=404, detail="One or more tags not found")

    # Create a new post
    post = Post(
        title=title,
        content=content,
        category_id=category_id,
        author_id=user.id,
        date_created=datetime.utcnow(),
        date_updated=datetime.utcnow(),
    )
    db.add(post)
    db.commit()

    # Link the post with the existing tags (PostTag relationships)
    # for tag_id in tags:
    #     post_tags = PostTag(post_id=post.id, tag_id=tag_id)
    #     db.add(post_tags)

    # db.commit()

    # Handle image saving for the post's main image
    single_image_folder = f"uploads/postimage/{post.id}"
    os.makedirs(single_image_folder, exist_ok=True)
    single_image_path = os.path.join(single_image_folder, image_url.filename)
    with open(single_image_path, "wb") as buffer:
        buffer.write(await image_url.read())
    post.image_url = single_image_path

    # Handle additional images for the post
    multiple_images_folder = f"uploads/features/{post.id}"
    os.makedirs(multiple_images_folder, exist_ok=True)
    for img in additional_images:
        img_path = os.path.join(multiple_images_folder, img.filename)
        with open(img_path, "wb") as buffer:
            buffer.write(await img.read())
        post_image = PostImage(post_id=post.id, image_url=img_path)
        db.add(post_image)

    db.commit()

    return {
        "success": True,
        "post_id": post.id,
        "main_image_url": post.image_url,
        "message": "Post created successfully",
    }