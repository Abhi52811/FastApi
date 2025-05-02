
from typing import List, Optional
from fastapi import APIRouter,HTTPException, Response, Depends, status
from sqlalchemy import func
from app import models, schemas
from .. import models,schemas,utils, oauth2
from ..databases import get_db
from sqlalchemy.orm import Session

router= APIRouter(
    prefix= "/posts",
    tags=['posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print("current_user: ", current_user)
    print("limit: ", limit)

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search), models.Post.owner_id == current_user.id)
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return results

@router.post("/createPosts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("current_user:",current_user)
    print(post.dict())
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    print(type(new_post))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=schemas.PostResponse)
def last_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).order_by(models.Post.created_At.desc()).first()
    return post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = (db.query(models.Post).filter(models.Post.id == id, models.Post.owner_id == current_user.id).first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    print(post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()