from fastapi import APIRouter, Depends, HTTPException, status, Path
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
#from routers import auth
# app = FastAPI()

router = APIRouter()

# models.Base.metadata.create_all(bind=engine)

# app.include_router(auth.router) ## include the auth router in the main app which is imported from the routers folder and access auth api from the main app

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(db: Session = Depends(get_db)):
    todo_list = db.query(models.Todo).all()
    return todo_list


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: Annotated[int, Path(gt=0,default=None)], db: Session = Depends(get_db)):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_item


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
    new_todo = models.Todo(**todo_request.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    if new_todo is not None:
        return new_todo
    else:
        raise HTTPException(status_code=400, detail="Todo not created")


@router.put("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def update_todo(todo_id: Annotated[int, Path(gt=0,default=None)], todo_request: TodoRequest, db: Session = Depends(get_db)):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_item.title = todo_request.title
    todo_item.description = todo_request.description
    todo_item.priority = todo_request.priority
    todo_item.complete = todo_request.complete

    db.commit()
    return todo_item
 

@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: Annotated[int, Path(gt=0,default=None)], db: Session = Depends(get_db)):
    todo_item = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo_item is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    db.commit()

    return {"message": "Todo deleted successfully"}