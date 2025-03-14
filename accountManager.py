import secrets
import time
from datetime import timedelta
from typing import Type

from flask import Response, Request
from sqlalchemy import and_, func, insert, text, Result, Row
from sqlalchemy.orm import Session

import tables
import database
from tables import Authentication
TOKEN_DURATION = timedelta(7)

# userid: int # fuck sqlalchemy
def getAuthToken(userid):
    session: Session = database.getSession()

    query = session.query(tables.Authentication).where(tables.Authentication.user_id == userid)
    auth: Type[Authentication] | None = query.first()

    if auth is None:
        print("creating token")
        token: str
        while True:
            token = secrets.token_hex()
            if session.query(tables.Authentication).where(tables.Authentication.token == token).first() is None:
                break
        session.execute(insert(Authentication), [{"token": token, "user_id": userid}])
        session.commit()
        session.close()
        return token

    token = auth.token # type: ignore
    print("updating token")
    query.update({"time_created": func.now()})
    session.commit()
    session.close()
    return token


def login(username: str, password:str) -> Response:
    print (username, password)
    session: Session = database.getSession()
    user: Type[tables.User] = session.query(tables.User).where(and_(tables.User.username == username, tables.User.password == password)).first()
    print(user)
    if user is None:
        session.close()
        return Response("username or password incorrect")
    session.close()
    response = Response("logged in")
    print(user.id)
    token = getAuthToken(int(user.id))
    print('token: ', token)
    response.set_cookie('token', token, httponly=True)
    return response


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


def getUser(request: Request) -> tables.User | None:
    token = request.cookies.get('token')
    if token is None:
        return None

    session: Session = database.getSession()
    return session.query(tables.User).where(tables.Authentication.token == token).join(tables.Authentication).first()


def getOrDefaultUserName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    else:
        return user.username