import json
import logging
import database

from flask import Response
from posts import postmanager
from tables import PostLike, User, Post

logger = logging.getLogger(__name__)

def deleteLike(postID, user: User):
    with database.getSession() as session:
        postQuery = postmanager.getPostQuery(session=session, postId=postID)

        if postQuery is None or postQuery.first() is None:
            return Response(status=401, response="Post not found")

        postLike = session.query(PostLike).where(PostLike.post_id == postID and PostLike.user_id == user.id).first()

        if postLike is None:
            return Response(status=400, response="You have not liked this post")
        
        session.delete(postLike)
        session.commit()
        
        likes = session.query(PostLike).where(PostLike.post_id == postID).count()

        postQuery.update({
            "likes": session.query(PostLike).where(PostLike.post_id == postID).count()
        })

        session.commit()
        
        return str(likes)

def addLike(postID: int, user: User):
    if user is None:
        response_data = json.dumps({"error": "You must be logged in to like a post"})
        return Response(status=401, response=response_data, mimetype='application/json')

    with database.getSession() as session:
        try:
            post = session.query(Post).filter(Post.id == postID).first()

            if not post:
                response_data = json.dumps({"error": "Post not found"})
                return Response(status=404, response=response_data, mimetype='application/json')

            existing_like = session.query(PostLike).filter(
                PostLike.post_id == postID,
                PostLike.user_id == user.id
            ).first()

            if existing_like:
                response_data = json.dumps({"likes": post.likes, "message": "You have already liked this post"})
                return Response(status=200, response=response_data, mimetype='application/json')

            postLike = PostLike(post_id=postID, user_id=user.id)
            session.add(postLike)

            session.flush()

            current_likes = session.query(PostLike).filter(PostLike.post_id == postID).count()
            post.likes = current_likes

            session.commit()

            response_data = json.dumps({"likes": current_likes})
            return Response(status=201, response=response_data, mimetype='application/json')

        except Exception as e:
            logger.error(f"Error adding like for post {postID} by user {user.id if user else 'None'}: {e}", exc_info=True)
            session.rollback()
            response_data = json.dumps({"error": "Could not process like request"})
            return Response(status=500, response=response_data, mimetype='application/json')

def getLike(postID, user: User):
    with database.getSession() as session:
        if user is not None:
            userLiked = (
                session.query(PostLike)
                .where((PostLike.post_id == postID) & (PostLike.user_id == user.id))
                .first()
                is not None
            )
        else:
            userLiked = False

        post = session.query(Post).where(Post.id == postID).first()

        return {
            "userLiked": userLiked,
            "likes": post.likes if post else 0
        }
    
def addShare(postID, user: User):
    with database.getSession() as session:
        if user is None:
            return Response(status=401, response="You must be logged in to share a post")
        
        post: Post | None = session.query(Post).where(Post.id == postID).first()
        post.shares += 1
        session.commit()
        
        return str(post.shares)