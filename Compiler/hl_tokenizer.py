import sys
import os
import re
import glob
from constant import *

class Tokenizer():

    def __init__(self, file_name):
        self.current_line = 0
        self.hl_file = open(file_name)
        self.current_command = []
        self.line_cursor = 0
        self.isPeeked = False
        self.peeked_token = None
    def read_line(self):
        self.line_cursor = 0
        while True:
            self.current_line += 1
            command = self.hl_file.readline()
            if not command:
                return None
            command = command.split('//') # earse comment
            command = command[0].strip()  # earse space and newline
            if len(command) == 0:
                continue
            command = re.split(r'(".*"|^class$|^constructor$|^function$|^method$|^field$|^static$|^var$|^int$|^char$|^boolean$|^void$|^true$|^false$|^null$|^this$|^let$|^do$|^if$|^else$|^while$|^return$\
                                |/\*|\*/|{|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~|\s*)',command)
            command = filter(None, command)
            return command
    
    def read_token(self):
        isComment = False
        if self.isPeeked:
            self.isPeeked = False
            return self.peeked_token
        while True:
            if self.line_cursor == len(self.current_command):
                self.current_command = self.read_line()
            if self.current_command == None:
                return None
            token = self.current_command[self.line_cursor]
            self.line_cursor += 1
            
            # not comment /* */
            if token == '/*':
                isComment = True
            elif token == '*/':
                isComment = False
                continue
            if isComment == True:
                continue
                
            # not space
            if SPACE_PATTERN.match(token):
                continue
            elif token in TOKEN_MAP:
                token = TOKEN_MAP[token]
            elif INTEGER_PATTERN.match(token):
                token = IntegerConstant(token)
            elif STRING_PATTERN.match(token):
                token = StringConstant(token)
            elif IDENTIFIER_PATTERN.match(token):
                token = Identifier(token)
            else:
                Exception('Unknown Token')
            return token

    def peek_token(self):
        self.peeked_token = self.read_token()
        self.isPeeked = True
        return self.peeked_token
        
        
        
        
        
        