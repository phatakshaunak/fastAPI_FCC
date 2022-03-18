from tabnanny import check
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, password_hashing, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/login", tags = ["Login"])

@router.post('/', response_model = schemas.Token)
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    email, password = user.username, user.password

    check_user = db.query(models.User).filter(models.User.email == email).first()

    if not check_user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    else:
        # Check if the hashed password is the same as that in the database
        if password_hashing.verify_password(password, check_user.password):
            
            # Create JWT Token
            access_token = oauth2.create_access_token(data = {"user_id": check_user.id})

            return {"access_token": access_token, "token_type": "bearer"}
    
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
