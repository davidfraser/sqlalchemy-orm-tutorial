#!/usr/bin/env python

import code
import sys

class ReadLineConsole(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>", histfile=None):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.queue = open("blogapp.py").readlines()
        try:
            import readline
        except ImportError:
            pass
        else:
            try:
                import rlcompleter
                self.completer = rlcompleter.Completer(locals)
                readline.set_completer(self.complete)
            except ImportError:
                pass
            readline.parse_and_bind("tab: complete")

    def complete(self, text, state):
        if text == '':
            if state == 0:
                return self.queue.pop(0).rstrip("\n")
            return None
        return self.completer.complete(text, state)
        
ldict = locals().copy()
ldict.pop("ReadLineConsole")
ldict.pop("code")
local_var_names = " ".join(sorted([var for var in ldict.keys() if not var.startswith("__")]))
console = ReadLineConsole(ldict)
banner = ("Python %s on %s\n(%s)" %
          (sys.version, sys.platform, local_var_names))
console.interact(banner=banner)

