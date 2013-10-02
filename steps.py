#!/usr/bin/env python

"""
doctest-based examples of working through the standard sqlalchemy tutorial. See README.md for further details
"""

if __name__ == "__main__":
    import doctest
    import sys
    doctest.testfile("steps%d.txt" % sys.version_info.major)


