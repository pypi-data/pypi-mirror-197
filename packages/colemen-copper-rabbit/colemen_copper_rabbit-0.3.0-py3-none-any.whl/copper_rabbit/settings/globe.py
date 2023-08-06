




from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import sessionmaker as _sessionmaker

base = declarative_base()



_engine = _create_engine(f"sqlite:///test.db")

_Session = _sessionmaker(bind=_engine)
_session = _Session()

session:Session = _session


# session:Session = None


# from sqlalchemy.orm import DeclarativeBase


# class Base(DeclarativeBase):
#     pass