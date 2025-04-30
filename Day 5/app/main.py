from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

import psycopg
from psycopg.rows import dict_row
import time

from sqlalchemy.orm import Session
from .databases import engine, get_db
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg.connect(host='localhost',dbname='fastapiDB',user='postgres',password='root',row_factory=dict_row)
        print(conn)
        cursor= conn.cursor()
        print(cursor)
        print("DB connection was sucessfull")
        break
    except Exception as error:
        print("Connection to DB failed")
        print("Error:",error)
        time.sleep(5) 

@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    test = db.query(models.Post)
    print(test)
    return {"stauts":posts}

@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post, db: Session = Depends(get_db)):
    # Method: 1
    # new_post = models.Post(title = post.title, content = post.content, published= post.published)
    # db.add(new_post)
    # Method: 2
    print(post.dict())
    # unpacking: **post.dict()
    for key, value in post.dict().items():
        print(f"{key}: {value}")
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/latest")
def last_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_At.desc()).first()
    return {"post_detail": post}

@app.get("/posts/{id}")
def get_post_by_id(id: int,db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db)):
    # saving the query
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,updated_post: Post, db: Session = Depends(get_db)):
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
    return {"data": post_query.first()}