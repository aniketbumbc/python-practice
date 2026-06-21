from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv() # load env

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment")

engine = create_engine(database_url, echo=True, pool_pre_ping=True)

LocalSession = sessionmaker(autoflush=False, autocommit = False, bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()

try:
    with engine.connect() as conn:
        print("DB connection successful!")
except Exception as e:
    print(f"DB connection failed: {e}")

