import secrets
from datetime import timedelta
from typing import Type

from flask import Request
from sqlalchemy import and_, func, insert
from sqlalchemy.orm import Session

import database
import globals
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


def login(username: str, password: str) -> str | None:
    if username == globals.ADMIN["account_name"]:
        raise Exception("Cannot get token for admin")
    session: Session = database.getSession()
    user: Type[tables.User] = session.query(tables.User).where(
        and_(tables.User.account_name == username, tables.User.password == password)
        ).first()
    if user is None:
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
        user = tables.User(account_name=username, password=password)
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
    
    if token is globals.ADMIN_TOKEN:
        if isinstance(request, Request):
            if request.remote_addr != "127.0.0.1":
                print ("attempted admin login from", request.remote_addr)
                return None
            print("admin login from", request.remote_addr)
            return tables.User(**ADMIN)
    
    session: Session = database.getSession()
    return session.query(tables.User).where(tables.Authentication.token == token).join(tables.Authentication).first()


def getUserByName(accountName: int) -> tables.User | None:
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


def getOrDefaultDisplayNameName(user: tables.User) -> str:
    if user is None:
        return 'anonymous'
    else:
        return user.account_name
