from fastapi import APIRouter, HTTPException, status, Depends
from schemas import UserCreate, UserPrivate, UserUpdate, UserPublic,Token
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
import models
from database import get_db
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token,hash_password,verify_access_token, oauth2_scheme,verify_password,CurrentUser
from config import settings

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

    await db.delete(user)
    await db.commit()
