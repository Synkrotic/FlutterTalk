from flask import Response

import accountManager
import database
from posts import postmanager
from tables import PostLike, User, Post



def deleteLike(postID, user: User):
    with database.getSession() as session:
        postQuery = postmanager.getPostQuery(postID)
        if postQuery is None or postQuery.first() is None:
            return Response(status=401, response="Post not found")
        
        postLike = session.query(PostLike).where(PostLike.post_id == postID and PostLike.user_id == user.id).first()
        if postLike is None:
            return Response(status=400, response="You have not liked this post")
        
        session.delete(postLike)
        session.commit()
        
        likes = session.query(PostLike).where(PostLike.post_id == postID).count()
        postQuery.update({"likes": session.query(PostLike).where(PostLike.post_id == postID).count()})
        session.commit()
        
        return str(likes)
    
    
def addLike(postID, user: User):
    with database.getSession() as session:
        if user is None:
            return Response(status=401, response="You must be logged in to like a post")
        if session.query(PostLike) \
                .where(PostLike.post_id == postID and PostLike.user_id == user.id) \
                .first() is not None:
            return Response(status=200, response="You have already liked this post")
        
        postLike = PostLike(post_id=postID, user_id=user.id)
        session.add(postLike)
        session.commit()
        
        likes = session.query(PostLike).where(PostLike.post_id == postID).count()
        postmanager.getPostQuery(postID).update({"likes": session.query(PostLike).where(PostLike.post_id == postID).count()})
        session.commit()
        
        return str(likes)
    
def getLike(postID, user: User):
    with database.getSession() as session:
        userLiked: bool
        if user is not None:
            userLiked = session.query(PostLike) \
                            .where(PostLike.post_id == postID and PostLike.user_id == user.id) \
                            .first() is not None
        else:
            userLiked = False
        
        return {
            "userLiked": userLiked,
            "likes": session.query(Post).where(Post.id == postID).first().likes
        }
    
    
def addShare(postID, user: User):
    with database.getSession() as session:
        if user is None:
            return Response(status=401, response="You must be logged in to share a post")
        if session.query(PostLike) \
                .where(PostLike.post_id == postID and PostLike.user_id == user.id) \
                .first() is None:
            return Response(status=400, response="You have not liked this post")
        
        post: Post | None = session.query(Post).where(Post.id == postID).first()
        post.shares += 1
        session.commit()
        
        return str(post.shares)