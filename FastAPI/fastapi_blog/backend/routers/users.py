from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, BackgroundTasks
from schemas import UserCreate, UserPrivate, UserUpdate, UserPublic,Token,ChangePasswordRequest,ForgotPasswordRequest,ResetPasswordRequest
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import models
from database import get_db
from datetime import timedelta,UTC,datetime
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token,hash_password,verify_access_token, oauth2_scheme,verify_password,CurrentUser,generate_rest_token,hash_reset_token
from config import settings
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool
from image_util import process_profile_image
from sqlalchemy import delete as sql_delete
from email_utils import send_password_reset_email
from storage.supabase_client import supabase
import uuid

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.post("/", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User).where(func.lower(models.User.username) == user.username.lower()))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    result = await db.execute(select(models.User).where(func.lower(models.User.email) == user.email.lower()))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = models.User(
        username=user.username,
        email=user.email.lower(),
        password_hash= hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "id": str(user.id)},
        expires_delta=timedelta(minutes=settings.access_token_mins)
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPrivate)
async def get_me(current_user:CurrentUser):
    return current_user

@router.get("/", response_model=List[UserPublic], status_code=status.HTTP_200_OK)
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await db.get(models.User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return user


@router.patch("/{user_id}", response_model=UserPrivate, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user:CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)]
):
  

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Unauthorized to update user."
        )

    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if "username" in update_data and update_data["username"].lower() != user.username.lower():
        result = await db.execute(
            select(models.User).where(func.lower(models.User.username) == update_data["username"].lower())
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken."
            )

    if "email" in update_data and update_data["email"].lower() != user.email.lower():
        result = await db.execute(
            select(models.User).where(func.lower(models.User.email) == update_data["email"].lower())
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    for field, value in update_data.items():
        if field in ("email", "username"):
            setattr(user, field, value.lower())
        else:
            setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user:CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Unauthorized to delete user."
        )
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )
    
    old_filename = user.image_file

    await db.delete(user)
    await db.commit()

    if old_filename:
        try:
            supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
        except Exception:
            pass  # don't fail the request if old file cleanup fails


@router.patch("/{user_id}/picture", response_model=UserPrivate)
async def upload_profile_picture(
    user_id: int,
    file: UploadFile,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to update this user's picture."
        )

    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
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
        processed_content = await run_in_threadpool(process_profile_image, content)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not process image. Ensure the file is a valid image."
        )

    # process_profile_image always re-encodes to JPEG
    new_filename = f"{uuid.uuid4()}.jpg"
    path = f"profile_pics/{new_filename}"


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

    old_filename = user.image_file  # old key, not full URL

    user.image_file = path  # store full key (with folder prefix), not URL, in DB
    await db.commit()
    await db.refresh(user)

    if old_filename:
        try:
            supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
        except Exception:
            pass  # don't fail the request if old file cleanup fails

    return user




@router.delete("/{user_id}/picture", response_model=UserPrivate)
async def delete_user_picture(user_id: int, current_user: CurrentUser, db: Annotated[AsyncSession, Depends(get_db)]):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to delete this user's picture."
        )

    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found."
        )

    if not user.image_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no profile picture to delete."
        )

    old_filename = user.image_file
    user.image_file = None
    await db.commit()
    await db.refresh(user)

    try:
        supabase.storage.from_(settings.supabase_bucket).remove([old_filename])
    except Exception:
        pass  # don't fail the request if old file cleanup fails

    return user


@router.post("/forgot_password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(
    payload: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(models.User).where(func.lower(models.User.email) == payload.email.lower()))
    user = result.scalars().first()

    if user:
        await db.execute(sql_delete(models.PasswordRestToken).where(models.PasswordRestToken.user_id == user.id),)

        raw_token = generate_rest_token()
        token_hash = hash_reset_token(raw_token)
        expires_at = datetime.now(UTC) + timedelta(minutes=settings.reset_token_expire_minutes)

        reset_token = models.PasswordRestToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        db.add(reset_token)
        await db.commit()

        background_tasks.add_task(send_password_reset_email, user.email, user.username, raw_token)

    return {"message": "If an account with that email exists, a password reset link has been sent."}



@router.post("/rest_password", status_code=status.HTTP_200_OK)
async def reset_password(
    payload: ResetPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    token_hash = hash_reset_token(payload.token)

    result = await db.execute(
        select(models.PasswordRestToken).where(models.PasswordRestToken.token_hash == token_hash)
    )
    reset_token = result.scalars().first()

    if not reset_token or reset_token.expires_at.replace(tzinfo=UTC) < datetime.now(UTC):
        await db.delete(reset_token)
        await db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )

    user = await db.get(models.User, reset_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token."
        )

    user.password_hash = hash_password(payload.new_password)

    await db.execute(sql_delete(models.PasswordRestToken).where(models.PasswordRestToken.user_id == user.id))

    await db.commit()

    return {"message": "Password has been reset successfully."}


@router.post("/me/password", status_code=status.HTTP_200_OK)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect."
        )

    current_user.password_hash = hash_password(payload.new_password)
    await db.execute(sql_delete(models.PasswordRestToken).where(models.PasswordRestToken.user_id == current_user.id))

    await db.commit()

    return {"message": "Password has been changed successfully."}