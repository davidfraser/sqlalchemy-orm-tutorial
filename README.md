sqlalchemy-orm-tutorial
=======================

Example of working through the standard [sqlalchemy](http://www.sqlalchemy.org) [ORM tutorial](http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html) for release `0.7`

This is to accompany an *Introduction to SQLAlchemy* talk originally done by David Fraser at [PyConZA 2012](http://za.pycon.org)

To start, run `pip install -r requirements.txt` (ideally from within a clean virtual environment). The code is in doctest format in `steps.txt`, and in plain python code in `blogapp.py`. If you run `try.py` it will give you a python interpreter with hacked `readline` support that allows you to follow one line at a time (press tab on a blank line to get the next line).

This is currently Python 2-compatible, but only because of print() and except and doctests - it should be easily adjustable to Python 3.
