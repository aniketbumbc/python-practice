from typing import Annotated,List
from fastapi import APIRouter
from fastapi import FastAPI,Request,HTTPException,status,Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse, PostUpdate
from sqlalchemy import select
import models
from database import Base, engine,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

# get list of all based on userID

@router.get("/{user_id}/posts", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Check user exists first
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Fetch all posts for that user
    posts = db.execute(
        select(models.Post).where(models.Post.user_id == user_id)
    ).scalars().all()
    
    return posts




@router.get("/", response_model=list[PostResponse], name="posts")
def home(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.execute(
        select(models.Post).where(models.Post.id == post_id)
    ).scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    # Verify user exists
    user = db.get(models.User, post.user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {post.user_id} not found"
        )
    
    new_post = models.Post(
        title=post.title,
        content=post.content,
        topic=post.topic,
        user_id=post.user_id
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    return post

  # add this import

@router.patch("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    post = db.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    # Only update fields that were provided (exclude_unset=True)
    update_data = post_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    post = db.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    db.delete(post)
    db.commit()
    
    return None  # 204 returns no body