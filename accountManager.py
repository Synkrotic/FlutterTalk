from sqlalchemy import and_
from sqlalchemy.orm import Session

import tables
import database


def login(username: str, password:str) -> bool:
    query = database.getSession().query(tables.User).filter(
        and_(tables.User.username == username, tables.User.password == password)
    )
    return query.first() is not None



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