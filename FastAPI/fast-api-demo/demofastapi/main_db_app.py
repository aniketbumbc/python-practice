from fastapi import FastAPI, Depends,HTTPException
from db import get_db, engine
from sqlalchemy.orm import Session
import model
from schema import LabBookStore,UpdateLabBookStore,PatchLabBookStore

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

@app.get("/labbooks/{book_id}")
def get_book_by_id(book_id:int,db:Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@app.put("/labbooks/{book_id}")
def update_book(book_id:int,updated_book: UpdateLabBookStore,db:Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    

    book.title = updated_book.title
    book.author = updated_book.author
    book.publish_date = updated_book.publish_date
    db.commit()
    db.refresh(book)
    return {
        "Message": "Book Update Successfully",
        "Book": book
    }

#A PATCH request is used when you want to update only the fields provided by the client, 
# instead of replacing the entire resource.

@app.patch("/labbooks/{book_id}")
def update_book(book_id:int,updated_book: PatchLabBookStore,db:Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    

    update_data = updated_book.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return {
        "message": "Book filed updated successfully",
        "book": book
    }


@app.delete("/labbooks/{book_id}")
def delete_book(book_id:int,db:Session = Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()

    return {
        "message": f"Book deleted successfully with name {book.title}"
    }