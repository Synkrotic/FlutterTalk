from typing import Type

from sqlalchemy import and_, delete
from sqlalchemy.orm import Query

import accountManager
from accountManager import getUserByName

import database
import tables
from tables import Following



def getUserDict(user: tables.User) -> dict:
    return {
        "displayName": accountManager.getOrDefaultDisplayName(user),
        "accountName": accountManager.getOrDefaultUserName(user),
        "bio": user.bio,
        "location": user.location,
        "pfp": "https://i.pinimg.com/736x/c0/27/be/c027bec07c2dc08b9df60921dfd539bd.jpg",
        "banner_color": user.banner_color,
        "likedAmount": user.likes,
        "followersAmount": user.followers
    }


def updateFollowers(user: tables.User, session: database.Session):
    amount = session.query(tables.Following).filter_by(following_id = user.id).count()
    user.followers = amount
    session.merge(user)  # Make sure to merge the updated user object
    session.commit()

    return amount


def updateLikes(user: tables.User, session: database.Session) -> int:
    amount = session.query(tables.PostLike).where(tables.PostLike.user_id == user.id).count()
    user.likes = amount
    session.merge(user)
    session.commit()
    return amount
    

def getFollowingPosts(user: tables.User, session: database.Session) -> Query:
    return session.query(tables.Post)\
        .join(tables.Following, tables.Following.following_id == tables.Post.user_id)\
        .where(tables.Following.follower_id == user.id)


def addFollowing(user1: tables.User, user2: tables.User):
    if getFollowing(user1, user2):
        return False
    with database.getSession() as session:
        session.add(tables.Following(follower_id=user1.id, following_id=user2.id))
        updateFollowers(user2, session)
        session.commit()
    return True
    
    
def removeFollowing(user1: tables.User, user2: tables.User):
    with database.getSession() as session:
        following = session.query(tables.Following).filter_by(follower_id=user1.id, following_id=user2.id).first()
        if following:
            delete(Following).where(and_(Following.follower_id == user1.id, Following.following_id == user2.id))
            session.delete(following)
            updateFollowers(user2, session)
            session.commit()
        return True
        
        
def getFollowing(user: tables.User, user2: tables.User) -> bool:
    with database.getSession() as session:
        return session.query(tables.Following).where(and_(tables.Following.follower_id == user.id, tables.Following.following_id == user2.id)).first() is not None