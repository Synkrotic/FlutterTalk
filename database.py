import os
import sys

from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session

from tables import Base

engine: Engine = create_engine('sqlite:///' + os.path.join(os.getcwd(), 'data.sqlite'), echo=True)

def create() -> None:
    Base.metadata.create_all(engine)


def getSession() -> Session:
    return Session(engine)

def getConnection() -> Connection:
    return engine.connect()


if __name__ == '__main__':
    create()
    sys.exit(0)