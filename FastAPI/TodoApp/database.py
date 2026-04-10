from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/TodoAppDatabase"
engine = create_engine(SQLALCHEMY_DATABASE_URL) # each thread has its own database connection

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


