from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

class LABBOOK:
    id: int
    title: str
    author: str
    isPublished: bool

    def __init__(self, id, title, author, isPublished):
        self.id = id
        self.title = title
        self.author = author
        self.isPublished = isPublished
    





class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not present to created', default=None)
    title: str = Field(min_length=5,max_length=10)
    author: str = Field(min_length=3)
    isPublished: bool 

    model_config = {
            "json_schema_extra":{
                "example": {
                "title": "abc",
                "author": "test author",
                "isPublished": False
                }
            }
}






LAB_BOOKS = [

    LABBOOK(1,'Computer Sciences', 'codewithpi', True),
    LABBOOK(2,'Fast API Sciences', 'codewithpi', False),
    LABBOOK(3,'Computer Sciences-1', 'meApi', True),
    LABBOOK(5,'HP-1', 'greatHP', False),
    LABBOOK(5,'HP-2', 'greatHP', False),
]


@app.get('/labbook')
async def read_all_books():
    return LAB_BOOKS

@app.post('/create_book')
async def create_book(book_request:BookRequest):
    new_book = LABBOOK(**book_request.dict())
    LAB_BOOKS.append(get_book_id(new_book))
    return LAB_BOOKS


def get_book_id(labbook:LABBOOK):
        labbook.id = 1 if len(LAB_BOOKS) == 0 else LAB_BOOKS[-1].id + 1 
    
    
        return labbook