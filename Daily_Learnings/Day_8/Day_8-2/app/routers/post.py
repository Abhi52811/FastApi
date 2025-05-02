
from typing import List
from fastapi import APIRouter,HTTPException, Response, Depends, status
from app import models, schemas
from .. import models,schemas,utils, oauth2
from ..databases import get_db
from sqlalchemy.orm import Session

router= APIRouter(
    prefix= "/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    test = db.query(models.Post)
    print(test)
    return posts

# Pedantic model converts dictionary into the specific model
@router.post("/createPosts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    print(user_id)
    print(post.dict())
    for key, value in post.dict().items():
        print(f"{key}: {value}")
    new_post = models.Post(**post.dict())
    # new_post is a sqlachmey model and need to convert it into pedantic model
    print(type(new_post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=schemas.PostResponse)
def last_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.created_At.desc()).first()
    return post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id: int,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    print(post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()