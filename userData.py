from typing import Type

from sqlalchemy import and_
from sqlalchemy.orm import Query
from accountManager import getUserByName

import database
import tables



def getFollowingPosts(user: tables.User, session: database.Session) -> Query:
    print(user)
    return session.query(tables.Post)\
        .join(tables.Following, tables.Following.following_id == tables.Post.user_id)\
        .where(tables.Following.follower_id == user.id)


def addFollowing(user1: tables.User, user2: tables.User):
    if getFollowing(user1, user2):
        return False
    with database.getSession() as session:
        session.add(tables.Following(follower_id=user1.id, following_id=user2.id))
        session.commit()
    return True
        
def removeFollowing(user1: tables.User, user2: tables.User):
    with database.getSession() as session:
        following = session.query(tables.Following).filter_by(follower_id=user1.id, following_id=user2.id).first()
        if following:
            session.delete(following)
            session.commit()
        return True
        
        
def getFollowing(user: tables.User, user2: tables.User) -> bool:
    with database.getSession() as session:
        return session.query(tables.Following).where(and_(tables.Following.follower_id == user.id, tables.Following.following_id == user2.id)).first() is not None