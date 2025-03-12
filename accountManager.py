import secrets
import time
from datetime import timedelta

from flask import Response, Request
from sqlalchemy import and_, func, insert
from sqlalchemy.orm import Session

import tables
import database
from tables import Authentication
TOKEN_DURATION = timedelta(7)

def getAuthToken(userid: int) -> str:
    session: Session = database.getSession()

    query = session.query(tables.Authentication).where(tables.User.id == userid)
    if query.first() is None:
        token: str
        while True:
            token = secrets.token_hex()
            if session.query(tables.Authentication).where(tables.Authentication.token == token).first() is None:
                break
        session.execute(insert(Authentication), [{"token": token, "user_id": userid}])
        session.commit()
        session.close()
        return token

    query.update({"time_created": func.now()})
    session.commit()
    session.close()
    return query.first().token


def getUser(request: Request) -> tables.User | None:
    token = request.cookies.get('token')
    if token is None:
        return None

    session: Session = database.getSession()
    return session.query(tables.Authentication).where(tables.Authentication.token == token).first()

def getOrDefaultUserName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    else:
        return user.username


def login(username: str, password:str) -> Response:
    print (username, password)
    session: Session = database.getSession()
    query = session.query(tables.User).where(
        and_(tables.User.username == username, tables.User.password == password)
    ).
    if query.first() is None:
        session.close()
        return Response("username or password incorrect")
    session.close()

    response = Response("logged in")
    token = getAuthToken(query.first().id.real)
    response.set_cookie('token', token, max_age=TOKEN_DURATION.seconds, httponly=True)



def _checkExists(username: str) -> bool:
    session: Session = database.getSession()
    user = session.query(tables.User).filter(tables.User.username == username).first()
    if user is None:
        return False
    else:
        return True


def createAccount(username: str, password: str):
    if _checkExists(username):
        return False
    else:
        session: Session = database.getSession()
        user = tables.User(username=username, password=password)
        session.add(user)
        session.commit()
        return True

