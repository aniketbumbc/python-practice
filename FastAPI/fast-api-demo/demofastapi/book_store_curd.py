from fastapi import FastAPI,status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


books = [
    {
        "id": 1,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publish_date": "1960-07-11"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "publish_date": "1949-06-08"
    },
    {
        "id": 3,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publish_date": "1813-01-28"
    },
    {
        "id": 4,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10"
    },
    {
        "id": 5,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publish_date": "1937-09-21"
    }
]
app = FastAPI()


class Book(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str


class BookUpdate(BaseModel):
    title:str
    author:str
    publish_date:str



@app.get("/books")
def get_books():
    return books


@app.post("/create_book")
def create_book(book:Book):
    new_book = book.model_dump()
    books.append(new_book)

    return {
        "Message": f"Book Created Successfully {book.title}"
    }


@app.get("/books/{book_id}")
def get_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            return book
        
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")


@app.put("/book/{book_id}")
def update_book(book_id:int, update_book:BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book["title"] = update_book.title
            book["author"] = update_book.author
            book["publish_date"] = update_book.publish_date

            return {
        "Message":"Book Update Successfully"
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")


@app.delete("/book/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {
            "Message" : "Book Deleted Successfully"
            }
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book not found")

