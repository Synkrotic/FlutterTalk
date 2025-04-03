from datetime import datetime
from typing import Type
from sqlalchemy import not_, union_all
from sqlalchemy import not_, and_
from sqlalchemy.orm import Session, Query
from globals import *
from tables import Post, User, PostLike, CommentLink

import pytz
import accountManager
import database

def _getFormattedTime(posted: datetime) -> str:
    time = datetime.now(pytz.UTC) - posted
    if time.seconds < 60:
        return f"{time.seconds}s"
    elif time.seconds//60 < 60:
        return f"{time.seconds//60}m"
    elif time.seconds//60//60 < 24:
        return f"{time.seconds//60//60}h"
    else:
        return f"{time.days}d"

def __postClassToDict(posts: list[Type[Post]] | list[Post] | Post | Type[Post], user: User | None=None) -> list[dict] | dict:
    def convert(post: Post) -> dict:
        with database.getSession() as session:
            session.merge(post)

            comments = getComments(post, session)
            commentsView = __postClassToDict(comments, user)
            return {
                "postID": post.id,
                "accountName": post.user.account_name,
                "displayName": post.user.account_name,
                "content": post.content,
                "age": _getFormattedTime(post.time_created.replace(tzinfo=pytz.UTC)),
                "likeAmount": post.likes,
                "commentAmount": 0 if comments is None else len(comments),
                "sharedAmount": post.shares,
                "liked": user is not None and session.query(PostLike)
                    .where(and_(PostLike.post_id == post.id, PostLike.user_id == user.id)).first()
                         is not None,
                "comments": commentsView
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
        post: Post | None = session.query(Post).where(Post.id == current_post).first()
        if post is None:
            return None, cookies
        return __postClassToDict(post, accountManager.getUser(request)), cookies


def getPosts(amount: int, request: Request, subSet: Query | None = None) -> (dict, list[Cookie]):
    currentPost = 0
    if getCookie(request, 'current_post') is not None:
        currentPost = getCookie(request, 'current_post')
    cookies = addCookie([], Cookie("current_post", currentPost + amount))
    with database.getSession() as session:
        if subSet is not None:
            posts = subSet.where(not_(Post.has_parent)).offset(currentPost).limit(amount).all()
        else:
            posts = session.query(Post).where(not_(Post.has_parent)).offset(currentPost).limit(amount).all()
        if len(posts) == 0:
            print("no posts")
            return [], cookies
        return __postClassToDict(posts, accountManager.getUser(request)), cookies


def getPostsOfUserByID(userID: int, amount: int, request: Request) -> (dict, list[Cookie]):
    currentPost = 0
    if getCookie(request, 'current_post') is not None:
        currentPost = getCookie(request, 'current_post')
    cookies = addCookie([], Cookie("current_post", currentPost + amount))
    
    with database.getSession() as session:
        posts = session.query(Post).where(Post.id > currentPost, Post.user_id == userID).limit(amount).all()
        if len(posts) == 0:
            return [], cookies
        return __postClassToDict(posts, accountManager.getUser(request)), cookies


def getPostDict(postId: int, request: Request) -> dict | None:
    with database.getSession() as session:
        return __postClassToDict(session.query(Post).where(Post.id == postId).first(), accountManager.getUser(request))


def getPostQuery(session: Session, postId: int) -> Query | None:
    return session.query(Post).where(Post.id == postId)


def addPost(post: dict):
    with database.getSession() as session:
        post = Post(**post)
        session.add(post)
        session.commit()
        return post.id


def getComments(post: Post, session: Session | None = None) -> list[Type[Post]]:
    localSession = session is None
    if localSession:
        session = database.getSession()
    result = session.query(Post)\
            .join(CommentLink, CommentLink.comment == Post.id)\
            .filter(CommentLink.parent == post.id)\
            .all()
    if localSession:
        session.close()
    print(result)
    return result

