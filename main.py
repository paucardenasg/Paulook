import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Union, List

app = FastAPI()


class Posts(BaseModel):
    n_likes: int
    description: str
    user_id: int
    creation_date: Union[datetime, None] = None
    post_id: int
    title_post: str


class Users(BaseModel):
    user_name: str
    user_id: int
    user_age: int
    user_rol: str
    rol_id: int
    career: Union[str, None] = None
    semester: Union[str, None] = None
    friends: List[int]


posts_dict = {}
users_dict = {}


@app.put('/posts')
def create_post(post: Posts):
    post = post.dict()
    posts_dict[post['post_id']] = post
    return {'description': f'Post {post["post_id"]} creado correctamente.'}


@app.put('/users')
def create_user(user: Users):
    user = user.dict()
    users_dict[user['user_id']] = user
    return {'description': f'El user {user["user_id"]} con rol {user["user_rol"]} se creó correctamente.'}


@app.post('/users/{user_id}/{friend_id}')
def update_user(user_id: int, friend_id: int):
    main_user = users_dict[user_id]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
