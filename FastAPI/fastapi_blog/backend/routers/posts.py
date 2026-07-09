from typing import Annotated, List
from fastapi import APIRouter, HTTPException, status, Depends,Query, UploadFile
from schemas import PostCreate, PostResponse, PostUpdate,PaginatedPostResponse
from sqlalchemy import select,func
import models
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from auth import CurrentUser
from config import settings
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from image_util import process_blog_thumbnail
from storage.supabase_client import supabase
import uuid

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

# GET /api/posts/{user_id}/posts — returns paginated posts belonging to a specific user
@router.get("/{user_id}/posts", response_model=PaginatedPostResponse, status_code=status.HTTP_200_OK)
async def get_user_posts(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    count_result = await db.execute(
        select(func.count()).select_from(models.Post).where(models.Post.user_id == user_id)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(models.Post)
        .options(selectinload(models.Post.author))
        .where(models.Post.user_id == user_id)
        .order_by(models.Post.date_posted.desc())
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()

    has_more = skip + len(posts) < total
    return PaginatedPostResponse(
        posts=[PostResponse.model_validate(post) for post in posts],
        total=total,
        skip=skip,
        limit=limit,
        has_more=has_more,
    )


# GET /api/posts/ — returns all posts from all users
@router.get("/", response_model=PaginatedPostResponse, name="posts")
async def home(db: Annotated[AsyncSession, Depends(get_db)], skip:Annotated[int,Query(ge=0)] = 0, limit: Annotated[int, Query(ge=1, le=100)] = 10):
    count_result = await db.execute(select(func.count()).select_from(models.Post))
    total = count_result.scalar () or 0
    result = await db.execute(
        select(models.Post).options(selectinload(models.Post.author)).order_by(models.Post.date_posted.desc()).offset(skip).limit(limit)
    )
    posts = result.scalars().all()
    has_more = skip +len(posts) < total
    return PaginatedPostResponse(posts=[PostResponse.model_validate(post) for post in posts], total=total, skip=skip, limit=limit, has_more=has_more)


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

    old_filename = post.blog_image_file

    await db.delete(post)
    await db.commit()

    if old_filename:
        try:
            supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
        except Exception:
            pass  # don't fail the request if old file cleanup fails

    return None


# PATCH /api/posts/{post_id}/thumbnail — uploads/replaces a post's thumbnail image
@router.patch("/{post_id}/thumbnail", response_model=PostResponse)
async def upload_post_thumbnail(
    post_id: int,
    file: UploadFile,
    current_user: CurrentUser,
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
            detail="Not authorized to update this post's thumbnail."
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be an image."
        )

    content = await file.read()

    if len(content) > settings.max_upload_size_byt:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.max_upload_size_byt // (1024*1024)} MB."
        )

    try:
        processed_content = await run_in_threadpool(process_blog_thumbnail, content)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not process image. Ensure the file is a valid image."
        )

    # process_blog_thumbnail always re-encodes to JPEG
    new_filename = f"{uuid.uuid4()}.jpg"
    path = f"blog/thumbnail/{new_filename}"

    try:
        supabase.storage.from_(settings.supabase_bucket).upload(
            path,
            processed_content,
            file_options={"content-type": "image/jpeg"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )

    old_filename = post.blog_image_file  # old key, not full URL

    post.blog_image_file = path  # store full key (with folder prefix), not URL, in DB
    await db.commit()
    await db.refresh(post)

    if old_filename:
        try:
            supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
        except Exception:
            pass  # don't fail the request if old file cleanup fails

    return post


# DELETE /api/posts/{post_id}/thumbnail — removes a post's thumbnail image
@router.delete("/{post_id}/thumbnail", response_model=PostResponse)
async def delete_post_thumbnail(post_id: int, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await db.get(models.Post, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post's thumbnail."
        )

    if not post.blog_image_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post has no thumbnail to delete."
        )

    old_filename = post.blog_image_file
    post.blog_image_file = None
    await db.commit()
    await db.refresh(post)

    try:
        supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
    except Exception:
        pass  # don't fail the request if old file cleanup fails

    return post
