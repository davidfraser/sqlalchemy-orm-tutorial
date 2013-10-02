#!/usr/bin/env python

"""
doctest-based examples of working through the standard sqlalchemy tutorial. See README.md for further details
"""

if __name__ == "__main__":
    import doctest
    import sys
    if sys.version_info.major >= 3:
        doctest.testfile("steps3.txt")
    else:
        doctest.testfile("steps.txt")


