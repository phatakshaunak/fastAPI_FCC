from . import schemas, database, models
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from .config import settings

# SECRET_KEY
# Algorithm HS256
# Expiration Time for the Token

# openssl rand -hex 32
'''https://stackoverflow.com/questions/60738514/openssl-rand-base64-32-what-is-the-equivalent-in-python'''

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
SECRET_KEY = settings.jwt_s

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return jwt_token

def verify_access_token(token: str, credentials_exception: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token_id = verify_access_token(token, credentials_exception = credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_id.id).first()

    return user