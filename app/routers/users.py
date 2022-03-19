from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, password_hashing, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = '/users', tags = ["Users"])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Check if the email address has already been registered and throw exception if present
    duplicate = db.query(models.User).filter(models.User.email == user.email).first()

    if duplicate:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f'User with email address: {user.email} already registered')

    user.password = password_hashing.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
        
@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} not found")
    
    return user