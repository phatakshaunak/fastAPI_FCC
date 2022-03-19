from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix = "/vote", tags = ["Votes"])

# Submit or remove a vote on a post
@router.post("/", status_code = status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                      models.Votes.user_id == current_user.id)

    result = vote_query.first()

    if vote.drc == 1:
        if result:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                                detail = f"User {current_user.id} has already upvoted post with an id {vote.post_id}")
        
        new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)

        db.add(new_vote)
        db.commit()
        return {"message": "Added vote successfully"}
    
    elif vote.drc == 0:
        if not result:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f"Vote does not exist")
        
        else:
            vote_query.delete(synchronize_session = False)
            db.commit()
            return {"message": "Deleted vote successfully"}
    
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"Voting direction can be either zero or one")