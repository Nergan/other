from os import _exit, system
from typing import Iterable, Callable
        
        
class Cmd:
    def __init__(self, names, fun):
        if isinstance(names, str):
            names = (names,)
            
        self.names = set(name for name in names)
        self.fun = fun
        
        
class Loop:
    def __init__(self):
        self.cmds = [Cmd(('cls'), cls)]
        self.default = print
        self.placeholder = '> '
        self.ch = '/'
        self.help = None
        
        
    def add_cmd(self, cmd, fun):
        if not isinstance(cmd, Iterable):
            cmd = (cmd, fun)
            
        cmd = Cmd(cmd, fun)
        self.cmds.append(cmd)
        
        
    def run(self):
        try:
            while True:
                inp = input(
                    self.placeholder()
                    if isinstance(self.placeholder, Callable)
                    else self.placeholder
                )
                if inp:
                    if inp[0] == self.ch:
                        if len(inp) == 1:
                            print(self.help)
                            continue    
                        
                        inp = inp.split()                            
                        cmd = inp[0][1:]
                        args = inp[1:] if len(inp) else ()
                        
                        for cmd_i in self.cmds:
                            if cmd in cmd_i.names:
                                break
                        else:
                            print('unknown command')
                            continue
                        
                        try:
                            res = cmd_i.fun(*args)
                            if res:
                                print(res)
                        except TypeError:
                            print('error: incorrect count of arguments passed')
                        
                        continue            
                    print(self.default(inp))
        except KeyboardInterrupt:
            _exit(0)
        
        
def cls():
    system('cls')