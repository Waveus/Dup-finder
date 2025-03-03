import os
import sys
import hashlib
from typing import Optional
from enum import Enum

class Quantity(Enum):
    NONE = 0
    ONE = 1
    SOME = 2

class Arg:
    def __init__(self, arg_name: str, flag: str, args_num: Quantity, help_message = ""):
        self.name = arg_name
        self.flag = flag
        self.args_num = args_num
        self.enabled = False
        self.help = help_message
        
        if args_num == Quantity.NONE:
            self.value = None
        elif args_num == Quantity.ONE:
            self.value = ""
        elif args_num == Quantity.SOME:
            self.value = []

class ArgsResolver:
    def __init__(self, lista: list[Arg] = None):
        self.argList: list[Arg] = None
        print(type(self.argList))
    
def main():
    userPaths = make_paths()
    arg: list[Arg] = []
    arg.append(Arg("recursive", "--r", Quantity.NONE, "Flag that specifies whether the program should include subfolders when searching for duplicates."))
    arg.append(Arg("paths", "", Quantity.SOME, "Path of folders and files that should be scanned."))

def make_paths() -> Optional[list[str]]:
    
    sys_args: list[str] = sys.argv
    user_path: list[str] = []

    for arg in sys_args[1:]:
        absolute_path = os.path.abspath(arg)
        if os.path.exists(absolute_path) == True: 
            user_path.append(absolute_path)

    if (len(user_path) == 0):
        return None
    
    return user_path
    
def resolve_flags():
    sys_args: list[str] = sys.argv
    


if __name__ == "__main__":
    main()
    
