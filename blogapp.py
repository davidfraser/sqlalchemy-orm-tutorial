#!/usr/bin/env python

import sqlalchemy
sqlalchemy.__version__

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)

engine.execute("select 1").scalar()

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

User.__table__ # doctest: +NORMALIZE_WHITESPACE

User.__mapper__ # doctest: +ELLIPSIS

Base.metadata.create_all(engine)

ed_user = User('ed', 'Ed Jones', 'edspassword')
ed_user.name
ed_user.password
str(ed_user.id)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

ed_user = User('ed', 'Ed Jones', 'edspassword')
session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first() # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
our_user

