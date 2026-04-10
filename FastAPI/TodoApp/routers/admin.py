from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

        



@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all_todos(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized user")
    todo_list = db.query(models.Todo).all()
    return todo_list



@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(todo_id: Annotated[int, Path(gt=0,default=None)], user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized user")
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    db.commit()
    return {"message": "Todo deleted successfully"}