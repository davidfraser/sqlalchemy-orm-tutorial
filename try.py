#!/usr/bin/env python

import code
import sys

class ReadLineConsole(code.InteractiveConsole):
    BACK_CHAR = 'Z'
    def __init__(self, locals=None, filename="<console>", histfile=None):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.queue = open("blogapp.py").readlines()
        self.queue_pos = 0
        self.back_search = None
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
        # print (text, self.queue_pos, self.back_search, state)
        if text == '':
            if state == 0:
                if self.back_search is not None:
                    self.queue_pos -= self.back_search + 1
                    self.back_search = None
                if self.queue_pos >= len(self.queue):
                    return "# That's all, folks!"
                line = self.queue[self.queue_pos]
                self.queue_pos += 1
                return line.rstrip("\n")
            return None
        elif text == self.BACK_CHAR:
            if state == 0:
                self.back_search = 1 if self.back_search is None else self.back_search + 1
                back_pos = self.queue_pos - self.back_search
                back_line = self.queue[back_pos if back_pos >= 0 else 0]
                return self.BACK_CHAR + "0" + back_line.rstrip("\n")
            elif state == 1:
                back_pos = self.queue_pos - self.back_search - 1
                back_line = self.queue[back_pos if back_pos >= 0 else 0]
                return self.BACK_CHAR + "1" + back_line.rstrip("\n")
            return None
        self.back_search = None
        return self.completer.complete(text, state)
        
ldict = locals().copy()
ldict.pop("ReadLineConsole")
ldict.pop("code")
local_var_names = " ".join(sorted([var for var in ldict.keys() if not var.startswith("__")]))
console = ReadLineConsole(ldict)
banner = ("Python %s on %s\n(%s)" %
          (sys.version, sys.platform, local_var_names))
console.interact(banner=banner)

