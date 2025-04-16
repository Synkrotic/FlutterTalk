import json
import secrets
from datetime import timedelta
from typing import Type

import bcrypt
from flask import Request
from sqlalchemy import and_, func, insert
from sqlalchemy.orm import Session, InstrumentedAttribute
from werkzeug.exceptions import BadRequest

import database
import globals
import mediaManager
import tables
from globals import ADMIN
from tables import Authentication


TOKEN_DURATION = timedelta(7)


# userid: int # fuck sqlalchemy
def __getAuthToken(userid):
    if userid == globals.ADMIN["id"]:
        raise Exception("Cannot get token for admin")
    session: Session = database.getSession()
    
    query = session.query(tables.Authentication).where(tables.Authentication.user_id == userid)
    auth: Type[Authentication] | None = query.first()
    if auth is None:
        token: str
        while True:
            token = secrets.token_hex()
            if session.query(tables.Authentication).where(tables.Authentication.token == token).first() is None:
                break
        session.execute(insert(Authentication), [{"token": token, "user_id": userid}])
        session.commit()
        session.close()
        return token
    
    token = auth.token  # type: ignore
    query.update({"time_created": func.now()})
    session.commit()
    session.close()
    return token


def genPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def checkPassword(password: str, hashed: str | InstrumentedAttribute) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def login(username: str, password: str) -> str | None:
    if username == globals.ADMIN["account_name"]:
        raise Exception("Cannot get token for admin")
    session: Session = database.getSession()
    user: Type[tables.User] = session.query(tables.User).where(
        and_(tables.User.account_name == username)
        ).first()

    if user is None:
        session.close()
        return None

    if not checkPassword(password, user.password):
        session.close()
        return None
    session.close()
    token = __getAuthToken(user.id)
    
    return token


def _checkExists(username: str) -> bool:
    session: Session = database.getSession()
    user = session.query(tables.User).where(tables.User.account_name == username).first()
    if user is None:
        return False
    else:
        return True


def createAccount(username: str, password: str):
    if _checkExists(username):
        return False
    else:
        session: Session = database.getSession()
        user = tables.User(account_name=username, password=genPassword(password))
        session.add(user)
        session.commit()
        return True


def getUser(request: Request) -> tables.User | None:
    if request is not None:
        token = request.cookies.get('token')
    else:
        return None
    if token is None:
        return None
    if token == globals.ADMIN_TOKEN:
        if isinstance(request, Request):
            if request.remote_addr != "127.0.0.1":
                print ("attempted admin access from ", request.remote_addr)
                return None
            print("admin access from", request.remote_addr)
            return tables.User(**ADMIN)
    
    session: Session = database.getSession()
    return session.query(tables.User).where(tables.Authentication.token == token).join(tables.Authentication).first()


def getUserByName(accountName: int) -> tables.User | None | Type[tables.User]:
    session: Session = database.getSession()
    user: Type[tables.User] = session.query(tables.User).where(
        tables.User.account_name == accountName
    ).first()
    if user is None:
        return None
    else:
        return user


def getOrDefaultUserName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    else:
        return user.account_name


def getOrDefaultDisplayName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    elif user.display_name is None:
        return user.account_name
    else:
        return user.display_name


def updateProfile(request: Request):
    user = getUser(request)
    if user is None:
        return json.dumps({"errorText": "User is not logged in!"}), 401, {'ContentType': 'application/json'}, None
    if user.account_name != request.form["accountname"] and _checkExists(request.form["accountname"]):
        return 'name_exists', None
    
    with database.getSession() as session:
        user = session.merge(user)
        try:
            user.display_name = request.form["name"]
            user.bio = request.form["bio"]
            user.account_name = request.form["accountname"]
            user.location = request.form["location"]
            user.banner_color = request.form["banner_color"]
            url, _ = mediaManager.postMedia(request.files.get('pfp'), user, 'MEDIA')
            user.profile_pic = url if url is not None else user.profile_pic
        except BadRequest as e:
            return 'bad_request', None
        session.commit()
        session.flush()
    
        return 'success', {
            "displayName": user.display_name,
            "accountName": user.account_name,
            "bio": user.bio,
            "location": user.location,
            "bannerColor": user.banner_color,
            "pfp": "media/999999999999999999.png",
        }
