from datetime import UTC, datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_pass:str, hash_pass:str) -> bool:
    return pwd_context.verify(plain_pass,hash_pass)


def create_access_token(data:dict, expires_delta:timedelta | None)-> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_mins)

    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm
    )
    return encode_jwt


def verify_access_token(token:str) -> str | None: 

    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(),algorithms=[settings.algorithm],options={"require":["exp","sub"]})
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")

