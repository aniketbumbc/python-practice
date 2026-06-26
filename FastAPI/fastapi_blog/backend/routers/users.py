from fastapi import APIRouter
from fastapi import FastAPI,Request,HTTPException,status,Depends
from schemas import UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated, List
import models
from database import Base, engine,get_db

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db:Annotated[Session,Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.username == user.username))
    exiting_user = result.scalars().first()

    if exiting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exits"
        )
    

    result = db.execute(select(models.User).where(models.User.email == user.email))
    exiting_user = result.scalars().first()

    if exiting_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exits"
        )
    

    new_user = models.User(
        username=user.username,
        email= user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(
        select(models.User).where(models.User.id == user_id)
    ).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return user


