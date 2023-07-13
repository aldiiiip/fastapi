from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_database
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

@router.get("/privateposts", response_model=List[schemas.PostResponse])
def get_post(db: Session= Depends(get_database), current_user : int = Depends(oauth2.get_current_user)) :
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts #automatically serialize data into JSON

@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session= Depends(get_database), current_user : int = Depends(oauth2.get_current_user), 
             Limit: int= 10, skip: int = 0, search: Optional[str] = "") :
    # cursor.execute("""SELECT * FROM post""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    votings = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    

    return votings #automatically serialize data into JSON

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session= Depends(get_database), user_id: int =  Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    print(user_id.id)
    new_post = models.Post(owner_id = user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, response: Response, db: Session= Depends(get_database), user_id: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id)))
    # post_1 = cursor.fetchone()
    post_1 = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post_1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Post id:{id} does not exist")
        
    return post_1

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session= Depends(get_database), current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM post WHERE id = %s returning *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post id:{id} does not exist")
    
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostBase, db: Session= Depends(get_database), current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s returning *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post id:{id} does not exist")	
    
    if post.owner_id != int(current_user.id):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()