from flask import Response
from sqlalchemy import and_
from sqlalchemy.orm import Session

import tables
import database
def getAuthToken(userid: int) -> str:
    session: Session = database.getSession()

    query = session.query(tables.Authentication).where(tables.User.id == userid)
    if query.first() is not None:
        query.update({"user_id": userid})
        return query.first().token


def login(username: str, password:str) -> Response:
    session: Session = database.getSession()
    query = session.query(tables.User).where(
        and_(tables.User.username == username, tables.User.password == password)
    )
    session.close()
    if query.first() is None:
        return Response("username or password incorrect")
    response = Response("logged in")
    response



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

