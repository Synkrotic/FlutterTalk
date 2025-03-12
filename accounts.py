import secrets

from flask import Request
from sqlalchemy import DateTime, func

import database
import tables


def linkOrCreateSession(request: Request) -> str:
    session = database.getSession()
    token = request.cookies.get("session")
    if token is None:
        session = database.getSession()
        while True:
            token = secrets.token_hex(16)
            if session.query(tables.Authentication).filter(tables.Authentication.token == token).first() is None:
                break

        session.add(tables.Authentication(token=token, user_id=0))
        session.commit()
    session.upd
    return token