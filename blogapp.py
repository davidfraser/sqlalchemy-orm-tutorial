#!/usr/bin/env python

import sqlalchemy
sqlalchemy.__version__ 

from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=False)

engine.execute("select 1").scalar()

