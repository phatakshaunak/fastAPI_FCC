from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, password_hashing, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = '/users', tags = ["Users"])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    user.password = password_hashing.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(type(new_user))
    return new_user
        
@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} not found")
    
    return user