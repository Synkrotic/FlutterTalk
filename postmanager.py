import database
from tables import Post


def getPost(increment):
    with database.getSession() as session:
        post: Post | None = session.query(Post).filter(Post.id == increment).first()
        if post is None:
            return None
        post.comments.filter()
        return {
            "postID": post.id,
            "accountName": post.user.username,
            "displayName": post.user.username,
            "content": post.content,
            "likeAmount": post.likes,
            "commentAmount": len(post.comments),
            "sharedAmount": post.shares,
            "liked": post.comments
        }