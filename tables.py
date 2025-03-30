from datetime import datetime

import pytz
from sqlalchemy import ForeignKey, Column, Integer, Text, VARCHAR, DateTime, func, String, Boolean
from sqlalchemy.orm import declarative_base, relationship, Mapped



Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_name = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    bio = Column(Text)
    profile_pic = Column(String)
    location = Column(String)
    
    posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    post_likes = relationship('PostLike', back_populates='user', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    has_parent = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    forwards = Column(Integer, default=0)
    time_created = Column(DateTime, nullable=False, default=lambda: datetime.now(pytz.UTC))
    
    user = relationship('User', back_populates='posts')
    post_likes = relationship('PostLike', back_populates='post', cascade='all, delete-orphan')
    shares = Column(Integer, default=0)


class CommentLink(Base):
    __tablename__ = 'comment'
    parent_id = Column('parent_id', Integer, ForeignKey('post.id'))
    comment_id = Column('comment_id', Integer, ForeignKey('post.id'),  primary_key=True)
    
    parent = Column('parent', Integer, ForeignKey('post.id'))
    comment = Column('comment', Integer, ForeignKey('post.id'))
    

class PostLike(Base):
    __tablename__ = 'post_like'
    
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    
    post = relationship('Post', back_populates='post_likes')
    user = relationship('User', back_populates='post_likes')


class Authentication(Base):
    __tablename__ = 'authentication'
    
    token = Column(VARCHAR(16), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, unique=True)
    time_created = Column(DateTime, nullable=False, default=func.now())
