from fastapi import FastAPI, Depends
from db import get_db, engine
from sqlalchemy.orm import Session
import model
from schema import LabBookStore


app = FastAPI()

@app.post("/labbooks")
def create_book(book:LabBookStore, db:Session = Depends(get_db)):
    new_book = model.Book(title=book.title, author=book.author, publish_date=book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {
        "Message": "Book Successfully Added"
    }


@app.get("/labbooks")
def get_all_books(db:Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books