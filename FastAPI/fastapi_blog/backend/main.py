from contextlib import asynccontextmanager
from fastapi.exception_handlers import(http_exception_handler,request_validation_exception_handler)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import text
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import Base, engine, get_db
from routers import users, posts
import models  # noqa: F401 - needed for Base.metadata.create_all to detect models
from database import init_db,check_db_connection

# Create tables
# Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(_app:FastAPI):
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.driver()



app = FastAPI(
    title="Blog API",
    description="A simple blog API with users and posts",
    version="1.0.0"
)

from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# Static files & templates
app.mount("/media", StaticFiles(directory="media"), name="media")
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database unavailable: {e}",
        )