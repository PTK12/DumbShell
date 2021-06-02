from code import InteractiveConsole
import sys
import math
import re
import os

# Add your own modules here!
MODULE = """
import numpy as np
import Crypto
from Crypto.Util.number import *
""".split("\n")

class DumbShell:
    locale = sys.modules['__main__'].__dict__  

    def __init__(self, verbose=True, auto_indent=True, indent_style="|   ", width=None):
        """
verbose : Toggles prompt
auto    : Toggles auto indent (indent tracker goes crazy)
style   : How indents look
width   : Size of terminal (Leave blank for auto)
        """
        self.v = verbose
        self.auto = auto_indent
        self.style = indent_style 
        self.space = "    "
        if not auto_indent:
            self.space = self.style = ""
        self.width = width

    def retrieve(self):
        if self.width:
            return self.width
        else:
            try:
                width = os.get_terminal_size().columns
                if width < 1: # Incase something goes wrong
                    return 80
                return width
            except:
                return 80

    def calc(self, space):
        k = self.retrieve()
        return max(k // space, 1)

    def setup(self, mod=MODULE):
        """
Setup code that you'd like to be pre run
        """
        a = InteractiveConsole(locals=self.locale)    
        for i in mod:
            a.runsource(i)
        return a

    def prompt(self):
        """
Sends a prompt
        """
        print(""" 
 /===\\
/     \\ Pot's dumb shell
\\     / (incl. math, numpy, Crypto...)
 \\===/
Tip: Press <Tab> then <Enter> to come with suggestions
        """)
        
    def find(self, s, d):
        """
Finds some matches for possible code
        """
        return {k:v for k,v in d.items() if s in k}

    def big(self, iters):
        func = lambda x: len(x.__class__.__name__)
        a = b = 0
        for i, j in iters:
            a, b = max(a, len(i)), max(b, func(j))
        return a, b

    def pls(self, search = None):
        """
Outputs and finds some matches for possible code
        """
        kek = self.locale
        if search:
            kek = self.find(search, kek)
        thing = kek.items()
        if len(thing) > 8:
            num = self.calc(30)
            for i, (k, v) in enumerate(thing):
                print(f"{v.__class__.__name__[:12]:<12} {k[:16]:<16}|", end="")
                if i % num == num - 1 or i + 1 == len(thing):
                    print()
        else:
            b, a = self.big(thing)
            num = self.calc(b + a + 4)
            for i, (k, v) in enumerate(thing):
                print(f"{v.__class__.__name__[:a]:<{a}}  {k[:b]:<{b}} |", end="")
                if i % num == num - 1 or i + 1 == len(thing):
                    print()

    def detect_str(self, inp):
        """
Checks to see if theres an unfinished docstring

Maybe copying IDLE code wasn't a good idea...
        """
        a = re.findall(r'(?P<STRING>\'\'\'[^\'\\\\]*((\\\\.|\'(?!\'\'))[^\'\\\\]*)*(\'\'\')?|"""[^"\\\\]*((\\\\.|"(?!""))[^"\\\\]*)*(""")?|\'[^\'\\\\\\n]*(\\\\.[^\'\\\\\\n]*)*\'?|"[^"\\\\\\n]*(\\\\.[^"\\\\\\n]*)*"?)', inp)
        if a:
            a = a[-1][0]
            if a.startswith("'''") or a.startswith('"""'):
                if a[-3:] != a[:3] or len(a) < 6:
                    return False
        return True

    def run(self):
        if self.v:
            self.prompt()
        a = self.setup()
        while True:
            inp = input(">>> ")
            if inp.endswith("\t"):
                self.pls(inp[:-1].split(" ")[-1])
                continue
            d, buf, ind = a.runsource(inp), inp, inp.rstrip().endswith(":")
            
            while d:
                inp = input(f"{ind%100:>2}| " + self.style*ind)
                if inp.strip():
                    while not self.detect_str(buf + inp):
                        inp += "\n" + input(f"{ind%100:>2}| ")
                    buf += "\n" + self.space*ind + inp
                    d = a.runsource(buf)
                else:
                    ind = max(0, ind - 1)
                    if ind < 1 or not self.auto:
                        d = a.runsource(buf + "\n")
                
                if inp.rstrip().endswith(":"):
                    ind += 1

if __name__ == "__main__":
    shell = DumbShell()
    shell.run()
