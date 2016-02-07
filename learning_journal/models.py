from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    Unicode,
    UnicodeText,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False, unique=True)
    body = Column(UnicodeText)
    created = Column(DateTime, default=datetime.now)  # no () !
    edited = Column(DateTime, default=datetime.now)

    @classmethod
    def all(cls):
        query = DBSession.query(cls).order_by(cls.created.desc())
        return [entry for entry in query]

    @classmethod
    def by_id(cls, id):
        query = DBSession.query(cls).get(id)
        return query
