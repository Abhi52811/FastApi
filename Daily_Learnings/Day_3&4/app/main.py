from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

import psycopg
from psycopg.rows import dict_row
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


# def find_post(id: int):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#     return None


@app.get("/posts/latest")
def last_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    post = cursor.fetchone()
    return {"post_detail": post}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""",(str(id),))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s  RETURNING *""",(post.title,post.content,post.published,str(id)))
    post=cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    conn.commit()
    return {"data": post}