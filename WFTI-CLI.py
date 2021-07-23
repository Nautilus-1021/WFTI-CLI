from cmd import Cmd
import os

class WFTI_SHELL(Cmd):
    prompt = "[" + os.getcwd() + "] "

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == "__main__":
    WFTI_SHELL().cmdloop()
