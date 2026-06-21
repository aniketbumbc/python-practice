from pydantic import BaseModel
from sqlalchemy.orm import Session
from auth import auth_models, auth_schema,utils
from fastapi import FastAPI,Depends,HTTPException,status
from .auth_db import get_db
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm_jwt])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"username":username, "role":role}


@app.get("/protected")
def protected_route(current_user:dict = Depends(get_current_user)):
    return {"Message": f"Welcome to user {current_user['username']} and access protected route"}


def require_roles(allowed_roles:list[str]):
    def role_checker(current_user:dict = Depends(get_current_user)):
        user_role =  current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not enough permission")
        
        return current_user
    
    return role_checker
        


@app.get("/profile")
def get_user_profile(current_user:dict = Depends(require_roles(["admin"]))):
    return{"message": f"Profile of {current_user['username']}"}


@app.get("/user/dashboard")
def user_dashboard(current_user:dict = Depends(require_roles(["user"]))):
    return {"Message": "Welcome user"}

@app.get("/admin/dashboard")
def user_dashboard(current_user:dict = Depends(require_roles(["admin"]))):
    return {"Message": "Welcome Admin"}


@app.get("/admin/users", response_model=list[auth_schema.UserResponse])
def get_all_users(
    current_user: dict = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db),
):
    users = db.query(auth_models.User).all()
    return users