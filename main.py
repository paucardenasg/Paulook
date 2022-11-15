import uvicorn
from datetime import datetime
from typing import Union, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Posts(BaseModel):
    n_likes: int = Field(gt=-1)
    description: str = Field(min_length=1, max_length=140)
    user_id: int = Field(gt=-1)
    creation_date: Union[datetime, None] = None
    title_post: str = Field(min_length=1, max_length=100)


class Users(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    user_age: int = Field(gt=17, lt=121)
    role_id: int = Field(gt=-1)
    career: Union[str, None] = Field(min_length=1, max_length=100)
    semester: Union[int, None] = Field(gt=0, lt=13)
    friends: str = Field(min_length=1, max_length=100)


@app.put('/posts')
def create_post(post: Posts, db: Session = Depends(get_db)):
    post_model = models.Post()
    post_model.title_post = post.title_post
    post_model.n_likes = post.n_likes
    post_model.description = post.description
    post_model.user_id = post.user_id
    post_model.creation_date = post.creation_date
    db.add(post_model)
    db.commit()
    return {'description': f'Post creado correctamente.'}


@app.put('/users')
def create_user(user: Users, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.user_name = user.user_name
    user_model.user_age = user.user_age
    user_model.role_id = user.role_id
    user_model.career = user.career
    user_model.semester = user.semester
    user_model.friends = user.friends
    db.add(user_model)
    db.commit()
    return {'description': f'El usuario se creó correctamente.'}


@app.post("/users/{user_id}")
def update_user(user_id: int, user: Users, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {user_id} : Does not exist"
        )

    user_model.user_name = user.user_name
    user_model.user_age = user.user_age
    user_model.role_id = user.role_id
    user_model.career = user.career
    user_model.semester = user.semester
    user_model.friends = user.friends
    db.add(user_model)
    db.commit()
    return {"Description": f"Usuario con ID {user_id} modificado correctamente."}


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"The user with ID {user_id} does not exist."
        )
    return user_model


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)
