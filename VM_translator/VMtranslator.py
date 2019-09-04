import sys
import os
import re
import glob
from constant import *
from parser import Parser
from code_writer import Code_Writer

def main():
    file_path = sys.argv[1]
    dir_path = os.path.dirname(file_path)
    file_name = dir_path.split("/")[-1]
    files = glob.glob(dir_path+"/*.vm")
    code_writer = Code_Writer(dir_path+"/"+file_name+".asm")
    for file in files:
        parser = Parser(file)
        fileName = os.path.basename(file).split(".")[0]
        code_writer.set_current_file_name(fileName)
        while True:
            command_type, command = parser.read_command()
            if command_type == None:
                break
            elif command_type in [C_PUSH,C_POP]:
                code_writer.WritePushPop(command[0],command[1],command[2])
            elif command_type == C_ARITHMETIC:
                code_writer.WriteArithmetic(command[0])
            elif command_type == C_LABEL:
                code_writer.WriteLabel(command[1])
            elif command_type == C_GOTO:
                code_writer.WriteGoto(command[1])
            elif command_type == C_IF:
                code_writer.WriteIf(command[1])
            elif command_type == C_FUNCTION:
                code_writer.WriteFunction(command[1],command[2])
            elif command_type == C_RETURN:
                code_writer.WriteReturn()
            elif command_type == C_CALL:
                code_writer.WriteCall(command[1],command[2])

if __name__ == "__main__":
    main()
