sqlalchemy-orm-tutorial
=======================

Example of working through the standard [sqlalchemy](http://www.sqlalchemy.org) [ORM tutorial](http://docs.sqlalchemy.org/en/rel_0_8/orm/tutorial.html) for release `0.8`

This is to accompany an *Introduction to SQLAlchemy* talk originally done by David Fraser at [PyConZA 2012](http://za.pycon.org/2012/speaker/31/detail.html) and then done in a more appropriate tutorial style at [PyConZA 2013](http://za.pycon.org/talks/19/)

To start, run `pip install -r requirements.txt` (ideally from within a clean virtual environment). The code is in doctest format in `steps2.txt` and `steps3.txt`, and in plain python code in `blogapp2.py` or `blogapp3.py` (depending on Python version 2 or 3). If you run `try.py` it will give you a python interpreter with hacked `readline` support that allows you to follow one line at a time (press tab on a blank line to get the next line).

In order to run in Python3, you currently need to re-run `extract_code.py`, which will (amongst other things) generate the Python 3 files from the Python 2 versions.
