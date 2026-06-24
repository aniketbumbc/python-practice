
from typing import Annotated
from fastapi import FastAPI,Request,HTTPException,status,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine,get_db
from backend.routers import users

Base.metadata.create_all(bind=engine) # create tables from models


app = FastAPI()
app.include_router(users.router)


app.mount("/media",StaticFiles(directory="media"), name="media")

templates= Jinja2Templates(directory="templates")



@app.get("/",include_in_schema=False)
@app.get("/api/posts", response_model=list[PostResponse])
def home():
    return posts



@app.get("/home/template",include_in_schema=False)
def home(request:Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id:int):
    for post in posts:
        if post.get("id") == post_id:
            return post
        

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Post Id / Not Found")


@app.post("/api/posts",response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post:PostCreate):
    new_id = max (p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "topic": post.topic,
        "date_posted": "June 23, 2026"
    }

    posts.append(new_post)
    return new_post