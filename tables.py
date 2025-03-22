from sqlalchemy import ForeignKey, Column, Integer, Text, VARCHAR, DateTime, func
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    account_name = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    bio = Column(Text)
    profile_pic = Column(String)
    location = Column(String)

    posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    post_likes = relationship('PostLike', back_populates='user', cascade='all, delete-orphan')
    comment_likes = relationship('CommentLike', back_populates='user', cascade='all, delete-orphan')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    forwards = Column(Integer, default=0)

    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    post_likes = relationship('PostLike', back_populates='post', cascade='all, delete-orphan')
    shares = Column(Integer, default=0)
class Comment(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)

    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')
    comment_likes = relationship('CommentLike', back_populates='comment', cascade='all, delete-orphan')

class PostLike(Base):
    __tablename__ = 'post_like'

    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    post = relationship('Post', back_populates='post_likes')
    user = relationship('User', back_populates='post_likes')

class CommentLike(Base):
    __tablename__ = 'comment_like'

    post_id = Column(Integer, ForeignKey('comment.post_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    comment = relationship('Comment', back_populates='comment_likes')
    user = relationship('User', back_populates='comment_likes')


class Authentication(Base):
    __tablename__ = 'authentication'

    token = Column(VARCHAR(16), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    time_created = Column(DateTime, nullable=False, default=func.now())