from pydantic import BaseModel
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def get_hello():
    return {"message": "Welcome to test"}


#http://127.0.0.1:8000/greet/nike?city=baltimore
@app.get("/greet/{name}")
def greet_user(name:str, city:str):
    return {"message":f"Hello Welcome Fast Api {name} and city is {city}"}


class Student(BaseModel):
    name:str
    age:int
    city:str
    roll_number:int



@app.post("/create_student")
def create_student(student:Student):
    return {
        "message":"Student Created",
        "Student":student
    }