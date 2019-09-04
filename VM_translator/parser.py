import sys
import re
from constant import *

class Parser():
    def __init__(self, filepath):
        self.vm_file = open(filepath)

    def __exit__(self, exception_type, exception_value, traceback):
        self.vm_file.close()

    def read_command(self):
        while True:
            command = self.vm_file.readline()
            if not command:
                return None, None
            command = command.split('//') # earse comment
            command = command[0].strip()  # earse space and newline
            if len(command) != 0:
                command = command.split()
                if command[0] in ["add","sub","and","or","neg","not","eq","gt","lt"]:
                    command_type = C_ARITHMETIC
                elif command[0] == 'push':
                    command_type = C_PUSH
                elif command[0] == 'pop':
                    command_type = C_POP
                elif command[0] == 'label':
                    command_type = C_LABEL
                elif command[0] == 'goto':
                    command_type = C_GOTO
                elif command[0] == 'if-goto':
                    command_type = C_IF
                elif command[0] == 'function':
                    command_type = C_FUNCTION
                elif command[0] == 'return':
                    command_type = C_RETURN
                elif command[0] == 'call':
                    command_type = C_CALL
                return command_type, command
