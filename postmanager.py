from flask import Request

from globals import *
import database
from tables import Post

def __postClassToDict(posts: list[Post]) -> list[dict]:
     return [{
        "postID": post.id,
        "accountName": post.user.account_name,
        "displayName": post.user.account_name,
        "content": post.content,
        "likeAmount": post.likes,
        "commentAmount": len(post.comments),
        "sharedAmount": post.shares,
        "liked": True
    } for post in posts]


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
        return __postClassToDict([post])[0], cookies


def getPosts(amount: int, request: Request) -> (dict, list[Cookie]):
    cookies = []
    currentPost = 0
    if request.cookies.get('current_post') is not None:
        currentPost = request.cookies.get('current_post')
    else:
        cookies = addCookie([], Cookie("current_post", currentPost))

    with database.getSession() as session:
        posts = session.query(Post).filter(Post.id > currentPost).limit(amount).all()
        if len(posts) == 0:
            return [], cookies
        return __postClassToDict(posts), cookies


def getPost(postId: int):
    with database.getSession() as session:
        return __postClassToDict([session.query(Post).filter(Post.id == postId).first()])[0]