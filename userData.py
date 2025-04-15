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
        .where(tables.Following.following_id == user.id)


def addFollowing(user1: tables.User, user2str: str):
    user2: tables.User = getUserByName(user2str)
    with database.getSession() as session:
        session.add(tables.Following(follower_id=user1.id, following_id=user2.id))
        session.commit()
    return True
        
def removeFollowing(user1: tables.User, user2str: str):
    user2: tables.User = getUserByName(user2str)
    with database.getSession() as session:
        session.delete(tables.Following(follower_id=user1.id, following_id=user2.id))
        session.commit()
    return True
        
        
def getFollowing(user: tables.User, user2str: str) -> bool:
    user2: tables.User = getUserByName(user2str)
    with database.getSession() as session:
        return session.query(tables.Following).where(and_(tables.Following.follower_id == user.id, tables.Following.following_id == user2.id)).first() is not None