Introduction to SQLAlchemy
+++++++++++++++++++++++++++++

.. image:: sqlalchemy-logo-large.png

Introduction
============

* How to use SQLAlchemy
* Primarily as an ORM layer
* But also explaining the other parts
* Relational databases
* Python DBAPI
* ORM layers

Philosophy of SQLalchemy
========================

* Abstraction (leaky)
* But Hand-Coded
* Database Independence (SQL dialects, data types)
* Logical set of classes that relate to database constructs

SQLalchemy concept map
======================

* Engine <=> Database
* Session <=> Database Connection
* (Data Type) <=> Column Type
* Schemas: Table, Column, Index, ForeignKey, Sequence...
* SQL statements/xepressions: Select, Insert, Update, Join ...
* And so on...

ORM Tutorial (using ``declarative``)
====================================

Working through the standard tutorial from the documentation. Code on github, if you want to follow along

* Basics
* Querying
* Relationships
* Eagerness
* Deleting
* Bonus Round

Basics
======

* Importing declarative and setting up a table
* Creating records, adding and simple querying
* Record statuses, flushing and committing
* Rollback

Querying
========

* Querying - record objects, named tuples
* Aliases
* Filtering
* Ordering, selecting ranges, first/one/all
* Literal SQL
* Counting

Relationships
=============

* Declaring relationships with foreign keys
* Working with related records
* Querying with joins
* Table aliases
* Subqueries and mapping to entities
* exists, has, any
* Relationship operators

The importance of being eager
=============================

* Eager loading
* Joined load

Deleting
========

* Deleting
* Cascading

Bonus Round
===========

* Many to many relationships

Questions
=========

* What is your name?
* What is your favourite colour?

Other interesting topics
========================

* Concurrent connections and avoiding deadlocks
* You can replace anything on any layer
