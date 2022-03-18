from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/posts", tags = ["Posts"])


# Get all posts
@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Posts).all()

    return posts


# Create a post, return 201 for post created
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Posts(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#Get post by path parameter {id}
@router.get("/{id}", response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} was not found")
    
    return post
    

# Delete posts
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    delete_query = db.query(models.Posts).filter(models.Posts.id == id)

    if delete_query.first():
        delete_query.delete(synchronize_session = False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")


# Update posts
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    update_query = db.query(models.Posts).filter(models.Posts.id == id)

    if update_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    
    update_query.update(post.dict(), synchronize_session = False)

    db.commit()

    return update_query.first()