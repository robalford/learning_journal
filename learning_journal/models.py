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

from passlib.context import CryptContext

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

password_context = CryptContext(schemes=['pbkdf2_sha512'])


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(255), nullable=False, unique=True, index=True)
    password = Column(Unicode(255), nullable=False)

    @classmethod
    def by_name(cls, username, session=None):
        if session is None:
            session = DBSession
        query = session.query(cls).filter(cls.username == username)
        return query.one()  # not sure if this is the best way to do this

    def verify_password(self, password):
        return password_context.verify(password, self.password)

# revised during class -- added utcnow, onupdate, session=None stuff for
# querying methods

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), nullable=False, unique=True)
    body = Column(UnicodeText)
    created = Column(DateTime, default=datetime.utcnow)  # no () !
    edited = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        query = session.query(cls).order_by(cls.created.desc())
        return [entry for entry in query]

    @classmethod
    def by_id(cls, id, session=None):
        if session is None:
            session = DBSession
        query = session.query(cls).get(id)
        return query
