from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    { 'id':1, 'title':'title-1', 'author':'abc', 'category':'English'},
    { 'id':2,'title':'title-1', 'author':'par', 'category':'English'},
    { 'id':3,'title':'title-4', 'author':'xyz', 'category':'Maths'},
    { 'id':4,'title':'title-3', 'author':'abc', 'category':'Science'},
    { 'id':5,'title':'title-4', 'author':'par', 'category':'Maths'},
]



@app.get("/books")
async def get_all_books():
    return BOOKS

@app.get("/books/{book_title}")
async def get_book_by_id(book_title:str):
    match_books = []
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            match_books.append(book)

    if not match_books:
        return {'message': 'book not found'}

    
    return match_books

@app.get('/books/')
async def get_books_category(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    if not books_to_return:
        return {'message': 'no books found'}

    return books_to_return


@app.get("/books/{author}/")
async def read_author_category(author:str, category:str):
    books_found = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold() and book.get('category').casefold() == category.casefold():
            books_found.append(book)

    if not books_found:
        return {'message': 'Not Found'}
    
    return books_found