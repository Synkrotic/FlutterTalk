from typing import Type

from sqlalchemy.orm import Session, Query

import database
from globals import *
from tables import Post, User, PostLike


def __postClassToDict(posts: list[Type[Post]] | list[Post] | Post | Type[Post], user: User | None=None) -> list[dict] | dict:
    def convert(post: Post) -> dict:
        return {
            "postID": post.id,
            "accountName": post.user.account_name,
            "displayName": post.user.account_name,
            "content": post.content,
            "age": "0",
            "likeAmount": post.likes,
            "commentAmount": len(post.comments),
            "sharedAmount": post.shares,
            "liked": user is not None and Query(PostLike)
                    .filter(PostLike.post_id == post.id)
                    .filter(PostLike.user_id == user.id).first() is not None
        }
    
    if isinstance(posts, Post):
        return convert(posts)
    else:
        return [convert(post) for post in posts]


def getPostOfFeed(request) -> (dict | None, list[Cookie]):
    current_post = 0
    cookies = []
    if request.cookies.get('current_post') is not None:
        current_post = request.cookies.get('current_post')
    else:
        cookies = addCookie([], Cookie("current_post", current_post))
    with database.getSession() as session:
        post: Post | None = session.query(Post).filter(Post.id == current_post).first()
        if post is None:
            return None, cookies
        post.comments.filter()
        return __postClassToDict(post), cookies


def getPosts(amount: int, request: Request) -> (dict, list[Cookie]):
    currentPost = 0
    if getCookie(request, 'current_post') is not None:
        currentPost = getCookie(request, 'current_post')
    cookies = addCookie([], Cookie("current_post", currentPost + amount))
    
    with database.getSession() as session:
        posts = session.query(Post).filter(Post.id > currentPost).limit(amount).all()
        if len(posts) == 0:
            return [], cookies
        return __postClassToDict(posts), cookies


def getPost(postId: int):
    with database.getSession() as session:
        return __postClassToDict(session.query(Post).filter(Post.id == postId).first())

def getPostQuery(postId: int) -> (Session, Query | None):
    session: Session = database.getSession()
    return session, session.query(Post).filter(Post.id == postId)

def addPost(post: dict):
    with database.getSession() as session:
        post = Post(**post)
        session.add(post)
        session.commit()
        return

