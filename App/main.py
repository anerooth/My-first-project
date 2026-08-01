from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time
app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool = False

while True:
    try:
        conn = psycopg.connect(dbname='My first database',user='postgres',password="LOVE",row_factory=dict_row)
        cursor = conn.cursor()
        print("database connetion sucessfull")
        break
    except Exception as error:
        print("connection to database failed!")
        print(f"Error: {error}")
        time.sleep(2)

my_posts = [{"name":"content of post 1","id":0},{"name":"content of post 2","id":1}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for i,p in enumerate(my_posts):
        if (id == p['id']):
            return i

@app.get("/")
def read_root():
    return {"Hello":"world"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data":posts}

# @app.get("/posts")
# def get_posts():
#     return {"here are your posts"}

@app.get("/songs")
def fav_song():
    return{"My fav song is ranjha"}

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



