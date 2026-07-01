import requests

BASE_URL = "http://localhost:8000/api"

# 1. Log in to get a token — adjust endpoint/fields to match your auth route
login_response = requests.post(
    f"{BASE_URL}/users/token",  # or /token, /login, etc. — check your actual route
    data={"username": "", "password": ""},  # OAuth2PasswordRequestForm uses form data
)
login_response.raise_for_status()
token = login_response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

posts = [
    {"title": "Getting Started with FastAPI", "content": "FastAPI is a modern web framework for building APIs with Python.", "topic": "Web Development"},
    {"title": "Understanding Pydantic Models", "content": "Pydantic provides data validation using Python type annotations.", "topic": "Python"},
    {"title": "Async vs Sync in Python", "content": "Asynchronous programming allows Python to handle many tasks concurrently without blocking.", "topic": "Python"},
    {"title": "SQLAlchemy ORM Basics", "content": "SQLAlchemy lets you interact with databases using Python objects instead of raw SQL.", "topic": "Databases"},
    {"title": "Introduction to REST APIs", "content": "REST APIs use HTTP methods to perform operations on resources.", "topic": "Web Development"},
    {"title": "Docker for Beginners", "content": "Docker packages applications into containers for consistent deployment.", "topic": "DevOps"},
    {"title": "PostgreSQL vs MySQL", "content": "Both are popular relational databases, but they differ in features and performance.", "topic": "Databases"},
    {"title": "JWT Authentication Explained", "content": "JSON Web Tokens are a compact way to securely transmit information between parties.", "topic": "Security"},
    {"title": "Building a Blog API", "content": "A blog API typically includes endpoints for posts, comments, and users.", "topic": "Web Development"},
    {"title": "Python Virtual Environments", "content": "Virtual environments isolate project dependencies to avoid conflicts.", "topic": "Python"},
    {"title": "Dependency Injection in FastAPI", "content": "FastAPI's Depends system allows for clean and reusable dependency management.", "topic": "Web Development"},
    {"title": "Working with Alembic Migrations", "content": "Alembic handles schema migrations for SQLAlchemy-based projects.", "topic": "Databases"},
    {"title": "Error Handling Best Practices", "content": "Proper error handling improves API reliability and developer experience.", "topic": "Python"},
    {"title": "CORS Explained", "content": "Cross-Origin Resource Sharing controls how resources are requested from different domains.", "topic": "Web Development"},
    {"title": "Testing FastAPI Applications", "content": "Pytest and TestClient make it easy to write tests for FastAPI endpoints.", "topic": "Testing"},
    {"title": "Environment Variables in Python", "content": "Environment variables help manage configuration across different deployment environments.", "topic": "DevOps"},
    {"title": "Rate Limiting APIs", "content": "Rate limiting protects your API from abuse and ensures fair usage.", "topic": "Security"},
    {"title": "Caching Strategies", "content": "Caching can significantly improve API performance by reducing database load.", "topic": "Performance"},
    {"title": "GraphQL vs REST", "content": "GraphQL offers flexible queries, while REST relies on fixed endpoint structures.", "topic": "Web Development"},
    {"title": "Deploying FastAPI to Production", "content": "Uvicorn and Gunicorn are commonly used to serve FastAPI apps in production.", "topic": "DevOps"},
]

for i, post in enumerate(posts, 1):
    response = requests.post(f"{BASE_URL}/posts", json=post, headers=headers)
    print(f"{i}. Status: {response.status_code} - {post['title']}")