from typing import Annotated, List
from fastapi import APIRouter, HTTPException, status, Depends
from schemas import PostCreate, PostResponse, PostUpdate
from sqlalchemy import select
import models
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from auth import CurrentUser

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

# GET /api/posts/{user_id}/posts — returns all posts belonging to a specific user
@router.get("/{user_id}/posts", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_user_posts(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    result = await db.execute(
        select(models.Post).where(models.Post.user_id == user_id)
    )
    posts = result.scalars().all()

    return posts


# GET /api/posts/ — returns all posts from all users
@router.get("/", response_model=List[PostResponse], name="posts")
async def home(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(models.Post).options(selectinload(models.Post.author))
    )
    posts = result.scalars().all()
    return posts


# GET /api/posts/{post_id} — returns a single post by its ID
@router.get("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await db.get(models.Post, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post


# POST /api/posts/ — creates a new post for a given user_id
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate,current_user:CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):

    new_post = models.Post(
        title=post.title,
        content=post.content,
        topic=post.topic,
        user_id=current_user.id
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


# PATCH /api/posts/{post_id} — partially updates a post's fields (only provided fields are changed)
@router.patch("/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    current_user:CurrentUser,
    post_update: PostUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    post = await db.get(models.Post, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to update this post"
        )

    update_data = post_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    await db.commit()
    await db.refresh(post)

    return post


# DELETE /api/posts/{post_id} — deletes a post by its ID, returns 204 with no body
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user:CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await db.get(models.Post, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to delete this post"
        )

    await db.delete(post)
    await db.commit()

    return None
