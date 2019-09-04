import sys
import os
import re
import glob
from compile_engine import Compile_Engine

def main():
    file_path = sys.argv[1]
    dir_path = os.path.dirname(file_path)
    file_name = dir_path.split("/")[-1]
    files = glob.glob(dir_path+"/*.hl")
    for file in files:
        compiel_engine = Compile_Engine(file)
        #compiel_engine.test_command()
        compiel_engine.compile()

if __name__ == "__main__":
    main()
