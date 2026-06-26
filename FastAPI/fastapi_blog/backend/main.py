from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from database import Base, engine
from routers import users, posts
import models  # noqa: F401 - needed for Base.metadata.create_all to detect models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A simple blog API with users and posts",
    version="1.0.0"
)

# Static files & templates
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")