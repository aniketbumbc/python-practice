from pydantic import BaseModel
from sqlalchemy.orm import Session
import auth_models, auth_schema,utils
from fastapi import FastAPI,Depends,HTTPException,status
from auth_db import get_db
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


load_dotenv() # load env

secret_key = os.getenv("SECRET_KEY")
algorithm_jwt = os.getenv("ALGO")
expiry_time =  os.getenv("ACCESS_TOKEN_EXPIRY_TIME")

app = FastAPI()


def create_access_token(data:dict):
    to_encode_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(expiry_time))
    to_encode_data.update({'exp':expire}) # always keep exp as key to understand jwt it is expire time
    encode_jwt = jwt.encode(to_encode_data,secret_key,algorithm=algorithm_jwt)
    return encode_jwt

# signup user to app
@app.post("/signup")
def register_user(user:auth_schema.UserCreate, db: Session = Depends(get_db)):
    # check is user exit or not base on email or name
    is_user_exit = db.query(auth_models.User).filter(auth_models.User.email == user.email).first()
    if is_user_exit:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User email already exit")
    

    # hash password
    hash_password = utils.hash_password(user.password)

    # create new user instance

    new_user = auth_models.User(
        username = user.username,
        email = user.email,
        hashed_password = hash_password,
        role = user.role
    )

    #save user to DB
    db.add(new_user)
    db.commit()

    return {
        "Message":"User created successfully",
        "User":{
            new_user.id,
            new_user.username,
            new_user.email,
            new_user.role
        }
    }


@app.post("/login")
def login(form_data:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    # check is user exit or not base on email or name
    is_user_exit = db.query(auth_models.User).filter(auth_models.User.username == form_data.username).first()
    if not is_user_exit:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid User")
    
    if not utils.verify_password(form_data.password, is_user_exit.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Password")
    
    token_data = {'sub': is_user_exit.username, 'role': is_user_exit.role}
    token = create_access_token(token_data)
    return{"access_token":token, "token_type": "bearer"}




