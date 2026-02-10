from fastapi import FastAPI,Depends
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from typing import Annotated
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all_todos(db: db_dependency):
    todo_list = db.query(models.Todo).all()
    return todo_list


