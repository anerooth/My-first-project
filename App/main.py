from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class post(BaseModel):
    title: str
    content: str
    published: bool = False

while True:
    try:
        conn = psycopg.connect(dbname='My first database',user='postgres',row_factory=dict_row)
        cursor = conn.cursor()
        print("database connetion sucessfull")
        break
    except Exception as error:
        print("connection to database failed!")
        print(f"Error: {error}")
        time.sleep(2)

@app.get("/")
def read_root():
    return {"Hello":"world"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{"status":posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return{"data":posts}

@app.get("/songs")
def fav_song():
    return{"The creators fav song is ranjha"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(load:post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                                                                  (load.title,load.content,load.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"message":new_post}



@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return{"data":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post with id:{id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id :int,load : post):
    cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
                                                        (load.title,load.content,load.published,str(id)))
    conn.commit()
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your post with id:{id} was not found")

    return{"data":updated_post}
