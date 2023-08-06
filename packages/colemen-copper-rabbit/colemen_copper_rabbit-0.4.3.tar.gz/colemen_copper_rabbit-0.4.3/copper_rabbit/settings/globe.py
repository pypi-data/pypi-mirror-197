




from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine as _create_engine
from sqlalchemy import Engine
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker as _sessionmaker

base = declarative_base()
db = None
session:Session = None
engine:Engine = None






# session:Session = None


# from sqlalchemy.orm import DeclarativeBase


# class Base(DeclarativeBase):
#     pass