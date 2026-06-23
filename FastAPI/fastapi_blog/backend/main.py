from fastapi import FastAPI,Request,HTTPException,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import PostCreate, PostResponse

app = FastAPI()

templates= Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "title": "Getting Started with FastAPI",
        "topic": "Backend Development",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers automatic interactive documentation, high performance comparable to NodeJS and Go, and easy integration with async/await patterns.",
        "author": "Aniket Bhavsar",
        "date_posted": "2026-01-15"
    },
    {
        "id": 2,
        "title": "Building RAG Pipelines with LangChain",
        "topic": "GenAI Engineering",
        "content": "Retrieval-Augmented Generation (RAG) combines the power of vector databases with LLMs to provide context-aware responses. Using LangChain, you can build robust pipelines that chunk documents, embed them into a vector store, and retrieve relevant context at query time.",
        "author": "Jane Smith",
        "date_posted": "2026-02-03"
    },
    {
        "id": 3,
        "title": "React TypeScript Best Practices in 2026",
        "topic": "Frontend Development",
        "content": "TypeScript has become the standard for large-scale React applications. Key best practices include using strict mode, defining explicit prop interfaces, leveraging generics for reusable components, and using discriminated unions for complex state management.",
        "author": "Alex Johnson",
        "date_posted": "2026-03-22"
    },
    {
        "id": 4,
        "title": "JWT Authentication with FastAPI and SQLAlchemy",
        "topic": "Security",
        "content": "Implementing secure JWT-based auth involves generating access and refresh tokens, storing hashed passwords with bcrypt, protecting routes with OAuth2 dependency injection, and handling token expiry gracefully on both frontend and backend.",
        "author": "Maria Garcia",
        "date_posted": "2026-04-10"
    },
    {
        "id": 5,
        "title": "Deploying Next.js Apps with Docker and Neon DB",
        "topic": "DevOps",
        "content": "Containerizing a Next.js + FastAPI monorepo with Docker Compose simplifies environment parity across dev and prod. Using Neon DB as a serverless Postgres provider eliminates the need to manage a database container, reducing compose complexity and improving scalability.",
        "author": "Chris Lee",
        "date_posted": "2026-05-18"
    }
]


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