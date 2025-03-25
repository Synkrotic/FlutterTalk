import os
import sys

from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.orm import Session

from tables import Base

db_path = os.path.join(os.getcwd(), 'data.sqlite')
engine: Engine = create_engine(f'sqlite:///{db_path}', echo=True)

def create() -> None:
    # if not os.path.exists(db_path):
    Base.metadata.create_all(engine)

def getSession() -> Session:
    return Session(engine)

def getConnection() -> Connection:
    return engine.connect()

if __name__ == '__main__':
    create()
    sys.exit(0)