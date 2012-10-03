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

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first() # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
our_user
ed_user is our_user

session.add_all([
    User('wendy', 'Wendy Williams', 'foobar'),
    User('mary', 'Mary Contrary', 'xxg527'),
    User('fred', 'Fred Flinstone', 'blah')])
ed_user.password = 'f8s7ccs'
session.dirty
session.new  # doctest: +SKIP
session.commit()

ed_user.id # doctest: +NORMALIZE_WHITESPACE

ed_user.name = 'Edwardo'
fake_user = User('fakeuser', 'Invalid', '12345')
session.add(fake_user)

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all() #doctest: +NORMALIZE_WHITESPACE

session.rollback()
ed_user.name #doctest: +NORMALIZE_WHITESPACE
fake_user in session

session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all() #doctest: +NORMALIZE_WHITESPACE

for instance in session.query(User).order_by(User.id): # doctest: +NORMALIZE_WHITESPACE
    print instance.name, instance.fullname

for name, fullname in session.query(User.name, User.fullname): # doctest: +NORMALIZE_WHITESPACE
    print name, fullname

for row in session.query(User, User.name).all(): #doctest: +NORMALIZE_WHITESPACE
   print row.User, row.name

for row in session.query(User.name.label('name_label')).all(): #doctest: +NORMALIZE_WHITESPACE
   print(row.name_label)

from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all(): #doctest: +NORMALIZE_WHITESPACE
   print row.user_alias

