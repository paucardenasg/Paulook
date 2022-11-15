from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Post(Base):
    __tablename__ = "Post"

    post_id = Column(Integer, primary_key=True, index=True)
    post_title = Column(String)
    user_id = Column(Integer)
    post_description = Column(String)
    n_likes = Column(Integer)
    creation_date: Column(DateTime)


class User(Base):
    __tablename__ = "User"

    user_id: Column(Integer, primary_key=True, index=True)
    user_name: Column(String)
    user_age: Column(Integer)
    role_id: Column(Integer)
    career: Column(String)
    semester: Column(Integer)
    friends: Column(String)


class Role(Base):
    __tablename__ = "Role"

    role_id: Column(Integer, primary_key=True, index=True)
    role_description: Column(String)
