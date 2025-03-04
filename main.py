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
        self.help = help_message

        if args_num == Quantity.NONE:
            self.value = False
        elif args_num == Quantity.ONE:
            self.value = ""
        elif args_num == Quantity.SOME:
            self.value = []

class ArgsResolver:
    def __init__(self, arg_list: list[Arg] = None):
        self.argList: list[Arg] = arg_list if arg_list is not None else []

    def arg_resolve(self):
        
        for arg_list in self.argList:
            for i, arg_sys in enumerate(sys.argv[1:]):
                if arg_list.flag == arg_sys:
                    if arg_list.args_num == Quantity.NONE:
                        arg_list.value = True
                        break
                    if arg_list.args_num == Quantity.ONE:
                        if i + 1 < len(sys.argv[1:]) and not sys.argv[i + 2].startswith("-"):
                            arg_list.value = sys.argv[i+2]
                            break
                    if arg_list.args_num == Quantity.SOME:
                        j = 0
                        while i + j + 1 < len(sys.argv[1:]) and not sys.argv[i+ j + 2].startswith("-"):
                            arg_list.value.append(sys.argv[i + j +2])
                            j = j + 1
                        break
    
args : list[Arg] = [
    Arg("recursive", "-r", Quantity.NONE, "Flag that specifies whether the program should include subfolders when searching for duplicates."),
    Arg("paths", "-f", Quantity.SOME, "Path of folders and files that should be scanned."),
    Arg("hash", "-h", Quantity.SOME, "Specify which hash should be used to determine whether the file dyplicate exists.")
]

def main():
    resolver = ArgsResolver(args)
    resolver.arg_resolve()
    print(resolver.argList[1].value)
    

def make_paths(possiblepaths: list[str]) -> Optional[list[str]]:
    
    sys_args: list[str] = possiblepaths
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
    
