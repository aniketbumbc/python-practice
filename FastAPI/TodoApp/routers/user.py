from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from routers.auth import get_current_user



router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()



@router.get('/', status_code=status.HTTP_200_OK)
async def read_all_users(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized user")
    user_list = db.query(models.Users).all()
    return user_list



@router.get('/me', status_code=status.HTTP_200_OK)
async def read_current_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return user


