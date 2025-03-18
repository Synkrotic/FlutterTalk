import secrets
from datetime import timedelta
from typing import Type

from flask import Request
from sqlalchemy import and_, func, insert
from sqlalchemy.orm import Session

import database
import tables
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


def login(username: str, password:str) -> str | None:
    session: Session = database.getSession()
    user: Type[tables.User] = session.query(tables.User).where(and_(tables.User.username == username, tables.User.password == password)).first()
    if user is None:
        session.close()
        return None
    session.close()
    token = getAuthToken(user.id)

    return token


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


def getUser(request: Request | str) -> tables.User | None:
    if isinstance(request, str):
        token = request
    elif request is not None:
        token = request.cookies.get('token')
    else:
        return None

    if token is None:
        return None

    session: Session = database.getSession()
    return session.query(tables.User).where(tables.Authentication.token == token).join(tables.Authentication).first()


def getOrDefaultUserName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    else:
        return user.username