#!/usr/bin/env python

# To run these tests, simply run steps.py (with -v as an option if you want to see more details)

import sqlalchemy
sqlalchemy.__version__

# How to connect using a database URL - you may want to use echo=True for manual testing

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

# Running a simple SQL statement directly on the connection

engine.execute("select 1").scalar()

# Importing declarative and setting up a base class:

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Our first ORM record class:

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

User.__table__

User.__mapper__

# Actually creating the table:

Base.metadata.create_all(engine)

# An ORM record:

ed_user = User('ed', 'Ed Jones', 'edspassword')
ed_user.name
ed_user.password
str(ed_user.id)

# Sessions!

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()
our_user
ed_user is our_user

session.add_all([
    User('wendy', 'Wendy Williams', 'foobar'),
    User('mary', 'Mary Contrary', 'xxg527'),
    User('fred', 'Fred Flinstone', 'blah')])
ed_user.password = 'f8s7ccs'
session.dirty
session.new
session.commit()

ed_user.id

ed_user.name = 'Edwardo'
fake_user = User('fakeuser', 'Invalid', '12345')
session.add(fake_user)

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

session.rollback()
ed_user.name
fake_user in session

session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()

## That was Basic!

# Querying, objects or named tuples:

for instance in session.query(User).order_by(User.id):
    print instance.name, instance.fullname

for name, fullname in session.query(User.name, User.fullname):
    print name, fullname

for row in session.query(User, User.name).all():
   print row.User, row.name

# Aliasing query results:

for row in session.query(User.name.label('name_label')).all():
   print(row.name_label)

from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
   print row.user_alias

for u in session.query(User).order_by(User.id)[1:3]:
   print u

# Filtering

for name, in session.query(User.name).\
            filter_by(fullname='Ed Jones'):
   print name

for name, in session.query(User.name).\
            filter(User.fullname=='Ed Jones'):
   print name

for user in session.query(User).\
         filter(User.name=='ed').\
         filter(User.fullname=='Ed Jones'):
   print user

# Combination of some common filter operations, demonstrating the SQL that they produce:

session.query(User.fullname).\
         filter(User.name != 'wendy').\
         filter(User.name.like('%d%')).\
         filter(User.name.in_(['fred', 'mary'])).\
         filter(~User.name.in_(['jack'])).\
         order_by(User.id).all()

print session.query(User.name, User.name.in_(session.query(User.name).filter(User.name.like('%ed%')))).order_by('name').all()

print str(session.query(User.id).filter(User.name == None).filter(User.fullname != None))

from sqlalchemy import and_, or_
print session.query(User.name).filter(
        and_(
            or_(User.name.like('%ed%'), User.fullname.like('%y %')),
            User.password.like('%b%'))).\
        order_by(User.name).all()

# Different methods for handling results, requiring unique results etc:

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
query.all()

query.first()

# .one() doesn't let you have more than one result

from sqlalchemy.orm.exc import MultipleResultsFound
try:
    user = query.one()
except MultipleResultsFound, e:
    print e

from sqlalchemy.orm.exc import NoResultFound
try:
    user = query.filter(User.id == 99).one()
except NoResultFound, e:
    print e

# Literal SQL being interspersed with generated:

for user in session.query(User).\
            filter("id<224").\
            order_by("id").all():
    print user.name

session.query(User).filter("id<:value and name=:name").\
    params(value=224, name='fred').order_by(User.id).one()

session.query(User).from_statement(
                    "SELECT * FROM users where name=:name").\
                    params(name='ed').all()

session.query("id", "name", "thenumber12").\
        from_statement("SELECT id, name, 12 as "
                "thenumber12 FROM users where name=:name").\
                params(name='ed').all()

# Counting

session.query(User).filter(User.name.like('%ed')).count()

from sqlalchemy import func
session.query(func.count(User.name), User.name).group_by(User.name).all()

session.query(func.count('*')).select_from(User).scalar()

session.query(func.count(User.id)).scalar()

## That was querying!

# Relationships

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
 
    user = relationship("User", backref=backref('addresses', order_by=id))
 
    def __init__(self, email_address):
        self.email_address = email_address
 
    def __repr__(self):
        return "<Address('%s')>" % self.email_address

Base.metadata.create_all(engine)

# Working with related records

jack = User('jack', 'Jack Bean', 'gjffdd')
jack.addresses

jack.addresses = [
                Address(email_address='jack@google.com'),
                Address(email_address='j25@yahoo.com')]

jack.addresses[1]

jack.addresses[1].user

session.add(jack)
session.commit()

jack = session.query(User).\
filter_by(name='jack').one()
jack

jack.addresses

# Querying with joins

for u, a in session.query(User, Address).\
                    filter(User.id==Address.user_id).\
                    filter(Address.email_address=='jack@google.com').\
                    all():
    print u, a

session.query(User).join(Address).\
        filter(Address.email_address=='jack@google.com').\
        all()

# Table aliases

from sqlalchemy.orm import aliased
adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
    session.query(User.name, adalias1.email_address, adalias2.email_address).\
    join(adalias1, User.addresses).\
    join(adalias2, User.addresses).\
    filter(adalias1.email_address=='jack@google.com').\
    filter(adalias2.email_address=='j25@yahoo.com'):
    print username, email1, email2

# Subqueries: users with address record counts

from sqlalchemy.sql import func
stmt = session.query(Address.user_id, func.count('*').\
        label('address_count')).\
        group_by(Address.user_id).subquery()

for u, count in session.query(User, stmt.c.address_count).\
    outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
    print u, count

# Mapping subquery results to entities

stmt = session.query(Address).\
                filter(Address.email_address != 'j25@yahoo.com').\
                subquery()
adalias = aliased(Address, stmt)
for user, address in session.query(User, adalias).\
        join(adalias, User.addresses):
    print user, address

# Exists, any, has - does anything match?

from sqlalchemy.sql import exists
stmt = exists().where(Address.user_id==User.id)
for name, in session.query(User.name).filter(stmt):
    print name

for name, in session.query(User.name).\
        filter(User.addresses.any()):
    print name

for name, in session.query(User.name).\
    filter(User.addresses.any(Address.email_address.like('%google%'))):
    print name

session.query(Address).\
        filter(~Address.user.has(User.name=='jack')).all()

# Relationship operators

session.query(Address.email_address).\
        filter(Address.user == jack).\
        filter(Address.user != ed_user).\
        order_by(Address.id).all()

session.query(User.name).\
        filter(User.addresses.contains(address)).\
        filter(User.addresses.any(Address.email_address.like('%yahoo.com'))).\
        order_by(User.id).scalar()

session.query(Address.email_address).\
        filter(Address.user.has(name='ed')).\
        count()

session.query(Address).with_parent(jack, 'addresses').count()

## That was relationships

# Eager loading

from sqlalchemy.orm import subqueryload
jack = session.query(User).\
                options(subqueryload(User.addresses)).\
                filter_by(name='jack').one()
jack

jack.addresses

from sqlalchemy.orm import joinedload

jack = session.query(User).\
                       options(joinedload(User.addresses)).\
                       filter_by(name='jack').one()
jack

jack.addresses

from sqlalchemy.orm import contains_eager
jacks_addresses = session.query(Address).\
                            join(Address.user).\
                            filter(User.name=='jack').\
                            options(contains_eager(Address.user)).\
                            all()
jacks_addresses

jacks_addresses[0].user

## That was eager!

# Deleting and cascading

session.delete(jack)
session.query(User).filter_by(name='jack').count()

session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
 ).count()

session.rollback()
session.close()
session.query(User).filter_by(name='jack').count()

# Reconstructing without a new Base

User.cascading_addresses = relationship("Address", backref='cascading_user', cascade="all, delete, delete-orphan")

# load Jack by primary key
jack = session.query(User).get(5)

# remove one Address (lazy load fires off)
del jack.cascading_addresses[1]

# only one address remains
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count()

session.rollback()

## That was deleting and cascading!

# Many-to-many relationship

from sqlalchemy import Table, Text
# association table
post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)

class BlogPost(Base):
    __tablename__ = 'posts'
 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
 
    # many to many BlogPost<->Keyword
    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')
 
    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body
 
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

class Keyword(Base):
    __tablename__ = 'keywords'
 
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
 
    def __init__(self, keyword):
        self.keyword = keyword

from sqlalchemy.orm import backref
# "dynamic" loading relationship to User
BlogPost.author = relationship(User, backref=backref('posts', lazy='dynamic'))

Base.metadata.create_all(engine)

wendy = session.query(User).\
                filter_by(name='wendy').\
                one()
post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
session.add(post)

post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))

session.query(BlogPost).\
            filter(BlogPost.keywords.any(keyword='firstpost')).\
            all()

session.query(BlogPost).\
            filter(BlogPost.author==wendy).\
            filter(BlogPost.keywords.any(keyword='firstpost')).\
            all()

wendy.posts.\
        filter(BlogPost.keywords.any(keyword='firstpost')).\
        all()

