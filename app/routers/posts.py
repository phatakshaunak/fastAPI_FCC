from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix = "/posts", tags = ["Posts"])


# Get all posts
@router.get("/", response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).offset(skip).limit(limit).all()

    # To get only the user's posts
    # posts = db.query(models.Posts).filter(models.Posts.user_id == current_user.id).all()

    return posts


# Create a post, return 201 for post created
@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Posts(user_id = current_user.id, **post.dict())
    
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

    post = delete_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")

    if current_user.id != post.user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to do this action")
    
    else:
        delete_query.delete(synchronize_session = False)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)


# Update posts
@router.put("/{id}", response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    update_query = db.query(models.Posts).filter(models.Posts.id == id)

    post = update_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} does not exist")
    
    if current_user.id != post.user_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Not authorized to do this action")
    
    else:
        update_query.update(post.dict(), synchronize_session = False)

    db.commit()

    return update_query.first()