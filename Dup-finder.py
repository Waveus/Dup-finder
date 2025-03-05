import os
import sys
import hashlib

class FlagConfig:
    def __init__(self, flags: set[str]):

        if flags == None:
            flags = set()

        self.help = True if "-h" in flags else False
        self.recursive = True if "-r" in flags else False

class ArgParser:
    def __init__(self):
        self.files = set(filter(os.path.isfile, map(os.path.abspath, sys.argv[1:]))) or None
        self.dirs = set(filter(os.path.isdir, map(os.path.abspath, sys.argv[1:]))) or None
        self.flags = set(filter(lambda flag: flag.startswith("-"), sys.argv[1:])) or None

def main():
    Parser = ArgParser()
    Config = FlagConfig(Parser.flags)
    run(Parser, Config)

def run(Parser: ArgParser, Config: FlagConfig):

    files: list[str] = Parser.files
    dirs: list[str] = Parser.dirs
    file_sizes: dict[int, list[str]] = {} #size, file names, if len(list) > 1 -> make hash and compare hashes
    hashes_of_files: dict[str, list[str]] = {} #hash, file names

    NO_ARGS_PASSED = 1
    
    if Config.help == True or len(sys.argv) == NO_ARGS_PASSED:  
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        print("DESCRIPTION:")
        print("Script for finding file duplicates using a hash function.")
        print("\nUSAGE:")
        print("python3 Dup-finder.py <file>..<file> <folder>..<folder> -r | Find all duplicates in <file>'s and <folder>'s, including subfolders.")
        print("python3 Dup-finder.py <file>..<file>                       | Check if all the specified files are identical.")
        print("python3 Dup-finder.py <folder>..<folder> -r                | Check for duplicate files within the specified folder and its subfolders.")
        print("\nFLAGS:")
        print("Use -h to display help")
        print("Use -r to include subfolders in the scan")
        print("---------------------------------------------------------------------------------------------------------------------------------------")
        return
    
    if files == None:
        files = []
    if dirs == None:
        dirs = []

    get_file_sizes(files, dirs, file_sizes, Config.recursive)
    hash_files(file_sizes, hashes_of_files)
    print_results(hashes_of_files)

def get_file_sizes(files, dirs, file_sizes, recursive = False):
    for file in files:
        try:
            if os.path.getsize(file) not in file_sizes:
                file_sizes[os.path.getsize(file)] = []
            file_sizes[os.path.getsize(file)].append(file)
        except IOError as io:
            print("\n", io, "\n")

    for dir in dirs:                                        #commandline dirs
        for path, directories, dir_files in os.walk(dir):   #recursive dirs
            for file in dir_files:
                file_path = os.path.join(path, file)
                try:
                    if os.path.getsize(file_path) not in file_sizes:
                        file_sizes[os.path.getsize(file_path)] = []
                    file_sizes[os.path.getsize(file_path)].append(file_path)
                except IOError as io:
                    print("\n", io, "\n")

            if(recursive == False): 
                break
    
def hash_files(file_sizes, hashes_of_files):
    
    for files in file_sizes.values():
        if len(files) > 1:
            for file in files:
                try:
                    hashed_content = get_blake2hash(file)
                    if hashed_content not in hashes_of_files:
                        hashes_of_files[hashed_content] = []
                    hashes_of_files[hashed_content].append(file)
                except IOError as io:
                    print("\n", io, "\n")


def get_blake2hash(file_path):
    
    hash_blake2 = hashlib.blake2b()
    BLOCK_SIZE = 4096

    with open(file_path, "rb") as input_file:
        while block := input_file.read(BLOCK_SIZE):
            hash_blake2.update(block)
    return hash_blake2.hexdigest()

        
def print_results(hashes_of_files):
    
    for hash, files in hashes_of_files.items():
        if len(files) > 1:
            print("----------------------------")
            for file in files:
                print(file)
        
    

if __name__ == "__main__":
    main()
