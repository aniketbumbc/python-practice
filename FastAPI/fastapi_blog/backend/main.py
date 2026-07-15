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
from fastapi.middleware.cors import CORSMiddleware





# Create tables
# Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    await init_db()
    yield

app = FastAPI(
    title="Blog API",
    description="A simple blog API with users and posts",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://aniketdev.blog"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Routers
app.include_router(users.router)
app.include_router(posts.router)


#Registers the function as HTTP middleware on your FastAPI app. 
# Every HTTP request passes through this before hitting your route handlers, 
# And every response passes back through it on the way out.


# Register this function as HTTP middleware.
# Every request flows through here before reaching your route handlers,
# and every response flows back through on the way out to the client.
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    # Forward the request down the chain (next middleware -> your route handler)
    # and wait for the response. Everything below mutates that finished response.
    response = await call_next(request)

    # Anti-clickjacking: page may only be framed by the SAME origin.
    response.headers["X-Frame-Options"] = "SAMEORIGIN"

    # Stop browsers from MIME-sniffing the body and guessing a different
    # Content-Type than the one you declared.
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Set a sensible referrer default, but ONLY if a route/other layer
    # hasn't already set its own. Avoids overriding deliberate intent.
    if "Referrer-Policy" not in response.headers:
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # HSTS: force HTTPS for this domain + subdomains for max-age seconds
    # (63072000 = 2 years). Skipped on localhost/127.0.0.1 because sending
    # HSTS over local HTTP would pin HTTPS and lock you out of dev.
    if request.url.hostname not in ("localhost", "127.0.0.1"):
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains"
        )

    # Return the mutated response so it continues back to the client.
    # Omitting this is the classic bug — the request hangs.
    return response

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
