import os
import sys
import hashlib
from typing import Optional
from enum import Enum

class Quantity(Enum):
    NONE = 0
    ONE = 1
    ONEORMORE = 2

class Arg:
    def __init__(self, arg_name: str, flag: str, args_num: Quantity, default, help_message = ""):
        self.name = arg_name
        self.flag = flag
        self.args_num = args_num
        self.help = help_message
        self.value = default

class ArgsResolver:
    def __init__(self, arg_list: list[Arg] = []):
        self.arg_dict: dict[str, Arg] = {arg.flag: arg for arg in (arg_list or [])}

    def arg_resolve(self):
        for arg_list in self.arg_dict.values():
            for i, arg_sys in enumerate(sys.argv[1:]):
                if arg_list.flag == arg_sys:
                    if arg_list.args_num == Quantity.NONE:
                        arg_list.value = True
                        break
                    if arg_list.args_num == Quantity.ONE:
                        if i + 1 < len(sys.argv[1:]) and not sys.argv[i + 2].startswith("-"):
                            arg_list.value = sys.argv[i+2]
                            break
                    if arg_list.args_num == Quantity.ONEORMORE:
                        j = 0
                        arg_list.value.clear()
                        while i + j + 1 < len(sys.argv[1:]) and not sys.argv[i+ j + 2].startswith("-"):
                            arg_list.value.append(sys.argv[i + j + 2])
                            j = j + 1
                        break

    def make_folder_file_paths(self):
        possible_paths: list[str] = self.arg_dict["-p"].value
        possible_files: list[str] = self.arg_dict["-f"].value
        correct_files: list[str] = []
        correct_paths: list[str] = []

        for arg in possible_paths:
            absolute_path = os.path.abspath(arg)
            if os.path.exists(absolute_path) == True and os.path.isdir(absolute_path) == True: 

                correct_paths.append(absolute_path)

        if (len(correct_paths) == 0):
            self.arg_dict["-p"].value = []
        else:
            self.arg_dict["-p"].value = set(correct_paths)
            
            for file in possible_files:
                absolute_file_path = os.path.abspath(file)
                if os.path.isfile(absolute_file_path):
                    correct_files.append(absolute_file_path)

            for path in self.arg_dict["-p"].value:
                for file in self.arg_dict["-f"].value:
                    possible_file = os.path.join(path,file)
                    print(possible_file)
                    if os.path.isfile(possible_file):
                        correct_files.append(absolute_file_path)

            self.arg_dict["-f"].value = set(correct_files)    
                    
args : list[Arg] = [
    Arg("recursive", "-r", Quantity.NONE, False, "Flag that specifies whether the program should include subfolders when searching for duplicates."),
    Arg("paths", "-p", Quantity.ONEORMORE, ["."], "Path of folders that should be scanned."),
    Arg("hash", "-h", Quantity.ONE, "md5", "Specify which hash should be used to determine whether the file duplicate exists."),
    Arg("files", "-f", Quantity.ONEORMORE, ["*"], "Name of the files that should be compared with every file in the '-p' folder or its subfolders if '-r' enabled")
]

def main():
    resolver = ArgsResolver(args)
    resolver.arg_resolve()

    resolver.make_folder_file_paths()

    print(resolver.arg_dict["-r"].value)
    print(resolver.arg_dict["-p"].value)
    print(resolver.arg_dict["-h"].value)
    print(resolver.arg_dict["-f"].value)
    
if __name__ == "__main__":
    main()
    
