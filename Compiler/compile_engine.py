import sys
import os
import re
import glob
from hl_tokenizer import Tokenizer
from constant import *

class Compile_Engine():
    
    def __init__(self, in_file_path):
        self.in_file_path = in_file_path
        self.tokenizer = Tokenizer(in_file_path)
        self.nest_level = 0
        
    def write(self,command):
        white_space = ""
        for i in range(self.nest_level):
            white_space += "  "
        print white_space+command
    
    def Error(self,message):
        raise Exception(message + " at line " + str(self.tokenizer.current_line))
        
    def test_command(self):
        while True:
            command = self.tokenizer.read_line()
            if command == None:
                break
            print command
        
    def next_token_is(self,Tokens):
        token = self.tokenizer.peek_token()
        if token in Tokens:
            return True
        else:
            return False
            
    def next_token_type_is(self,Token_types):
        token = self.tokenizer.peek_token()
        if token.type in Token_types:
            return True
        else:
            return False

    def CompileKeyword(self,Tokens):
        token = self.tokenizer.read_token()
        if token in Tokens:
            self.write("<keyword> " + token.token + " </keyword>")
        else:
            self.Error('Unknown Keyword: ' + token.token)
            
    def CompileSymbol(self,Tokens):
        token = self.tokenizer.read_token()
        if token in Tokens:
            self.write("<symbol> " + token.token + " </symbol>")
        else:
            self.Error('Not Symbol: ' + token.token)
            
    def CompileIndentifier(self):
        token = self.tokenizer.read_token()
        if IDENTIFIER_PATTERN.match(token.token):
            self.write("<identifier> " + token.token + " </identifier>")
        else:
            self.Error('Not Identifier')
        return

    def compile(self):
        self.CompileClass()
        return
        
    def CompileClass(self):
        self.write("<class>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.CLASS])
        self.CompileClassName()
        self.CompileSymbol([Tokens.LEFT_CURLY_BRACKET])
        while True:
            if self.next_token_is([Tokens.STATIC,Tokens.FIELD]):
                self.CompileClassVarDec()
            elif self.next_token_is([Tokens.CONSTRUCTOR,Tokens.FUNCTION,Tokens.METHOD]):
                self.CompileSubroutineDec()
            elif self.next_token_is([Tokens.RIGHT_CURLY_BRACKET]):
                self.CompileSymbol([Tokens.RIGHT_CURLY_BRACKET])
                break
            else:
                self.ss('Unknown Token: ' + token.token)
        self.nest_level -= 1
        self.write("</class>")
        return
        
    def CompileClassName(self):
        self.CompileIndentifier()
        return
        
    def CompileClassVarDec(self): # ('static' | 'field') type varName (',' varName)* ';'
        self.write("<classVarDec>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.STATIC,Tokens.FIELD])
        self.CompileType()
        self.CompileVarName()
        while True:
            if self.next_token_is([Tokens.COMMA]):
                self.CompileSymbol([Tokens.COMMA])
                self.CompileVarName()
            elif self.next_token_is([Tokens.SEMI_COLON]):
                break
            else:
                self.Error("CompileClassVarDec Error")
        self.CompileSymbol([Tokens.SEMI_COLON])
        self.nest_level -= 1
        self.write("</classVarDec>")
        return
        
    def CompileSubroutineDec(self):
        self.write("<subroutineDec>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.CONSTRUCTOR,Tokens.FUNCTION,Tokens.METHOD])
        if self.next_token_is([Tokens.VOID,Tokens.CHAR,Tokens.INT,Tokens.BOOLEAN]):
            self.CompileKeyword([Tokens.VOID,Tokens.CHAR,Tokens.INT,Tokens.BOOLEAN])
        elif self.next_token_type_is([TokenType.IDENTIFIER]):
            self.CompileClassName()
        else:
            self.Error('CompileSubroutineDec Error')
        self.CompileSubroutineName()
        self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
        self.CompileParameterList()
        self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        self.CompileSubroutineBody()
        self.nest_level -= 1
        self.write("</subroutineDec>")
        
    def CompileParameterList(self):
        self.write("<parameterList>")
        self.nest_level += 1
        if not self.next_token_is([Tokens.RIGHT_ROUND_BRACKET]):
            self.CompileType()
            self.CompileVarName()
            while True:
                if self.next_token_is([Tokens.COMMA]):
                    self.CompileSymbol([Tokens.COMMA])
                    self.CompileType()
                    self.CompileVarName()
                elif self.next_token_is([Tokens.RIGHT_ROUND_BRACKET]):
                    break
                else:
                    self.Error('CompileParameterList Error')
        self.nest_level -= 1
        self.write("</parameterList>")
        
    def CompileSubroutineBody(self):
        self.write("<subroutineBody>")
        self.nest_level += 1
        self.CompileSymbol([Tokens.LEFT_CURLY_BRACKET])
        while True:
            if self.next_token_is([Tokens.VAR]):
                self.CompileVarDec()
            else:
                break
        self.CompileStatements()
        self.CompileSymbol([Tokens.RIGHT_CURLY_BRACKET])
        self.nest_level -= 1
        self.write("</subroutineBody>")
    
    def CompileSubroutineName(self):
        self.CompileIndentifier()
        return
        
    def CompileType(self):
        if self.next_token_is([Tokens.CHAR,Tokens.INT,Tokens.BOOLEAN]):
            self.CompileKeyword([Tokens.CHAR,Tokens.INT,Tokens.BOOLEAN])
        elif self.next_token_type_is([TokenType.IDENTIFIER]):
            self.CompileClassName()
        else:
            self.Error('CompileType Error')
        return
    
    def CompileVarName(self):
        self.CompileIndentifier()
        return
    
    def CompileVarNameMore(self):
        if self.next_token_is([Tokens.COMMA]):
            self.CompileSymbol([Tokens.COMMA])
            self.CompileVarName()
        return
        
    def CompileVarDec(self):
        self.write("<varDec>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.VAR])
        self.CompileType()
        self.CompileVarName()
        self.CompileVarNameMore()
        self.CompileSymbol([Tokens.SEMI_COLON])
        self.nest_level -= 1
        self.write("</varDec>")
        
    def CompileStatements(self):
        self.write("<statements>")
        self.nest_level += 1
        while True:
            if self.next_token_is([Tokens.LET]):
                self.CompileLet()
            elif self.next_token_is([Tokens.IF]):
                self.CompileIf()
            elif self.next_token_is([Tokens.WHILE]):
                self.CompileWhile()
            elif self.next_token_is([Tokens.DO]):
                self.CompileDo()
            elif self.next_token_is([Tokens.RETURN]):
                self.CompileReturn()
            elif self.next_token_is([Tokens.RIGHT_CURLY_BRACKET]):
                break
            else:
                self.Error("CompileStatements Error")
        self.nest_level -= 1
        self.write("</statements>")
    
    def CompileLet(self): # 'let' varName ('[' expression ']')? '=' expression ';'
        self.write("<letStatement>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.LET])
        self.CompileVarName()
        if self.next_token_is([Tokens.LEFT_BOX_BRACKET]):
            self.CompileSymbol([Tokens.LEFT_BOX_BRACKET])
            self.CompileExpression()
            self.CompileSymbol([Tokens.RIGHT_BOX_BRACKET])
        self.CompileSymbol([Tokens.EQUAL])
        self.CompileExpression()
        self.CompileSymbol([Tokens.SEMI_COLON])
        self.nest_level -= 1
        self.write("</letStatement>")
        
    def CompileIf(self): # 'if' '(' expression ')' '{' statements '}' ('else' '{' expression '}')?
        self.write("<ifStatement>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.IF])
        self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
        self.CompileExpression()
        self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        self.CompileSymbol([Tokens.LEFT_CURLY_BRACKET])
        self.CompileStatements()
        self.CompileSymbol([Tokens.RIGHT_CURLY_BRACKET])
        if self.next_token_is([Tokens.ELSE]):
            self.CompileKeyword([Tokens.ELSE])
            self.CompileSymbol([Tokens.LEFT_CURLY_BRACKET])
            self.CompileStatements()
            self.CompileSymbol([Tokens.RIGHT_CURLY_BRACKET])
        self.nest_level -= 1
        self.write("</ifStatement>")
        
    def CompileWhile(self): # 'while' '(' expression ')' '{' statements '}'
        self.write("<whileStatement>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.WHILE])
        self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
        self.CompileExpression()
        self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        self.CompileSymbol([Tokens.LEFT_CURLY_BRACKET])
        self.CompileStatements()
        self.CompileSymbol([Tokens.RIGHT_CURLY_BRACKET])
        self.nest_level -= 1
        self.write("</whileStatement>")
        
    def CompileDo(self): # 'do' subroutineCall ';'
        self.write("<doStatement>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.DO])
        self.CompileSubroutineName()
        if self.next_token_is([Tokens.LEFT_ROUND_BRACKET]): # subroutineCall -> subroutineName '(' expressionList ')'
            self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
            self.CompileExpressionList()
            self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        elif self.next_token_is([Tokens.DOT]):  # subroutineCall -> (className|varName) '.' subroutineName '(' expressionList ')'
            self.CompileSymbol([Tokens.DOT])
            self.CompileSubroutineName()
            self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
            self.CompileExpressionList()
            self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        else:
            self.Error("CompileDo Error")
        self.CompileSymbol([Tokens.SEMI_COLON])
        self.nest_level -= 1
        self.write("</doStatement>")
        
    def CompileReturn(self): # 'return' (expression)? ';'
        self.write("<returnStatement>")
        self.nest_level += 1
        self.CompileKeyword([Tokens.RETURN])
        if not self.next_token_is([Tokens.SEMI_COLON]):
            self.CompileExpression()
        self.CompileSymbol([Tokens.SEMI_COLON])
        self.nest_level -= 1
        self.write("</returnStatement>")
        
    def CompileExpression(self):
        self.write("<expression>")
        self.nest_level += 1
        self.CompileTerm()
        self.CompileTermMore()
        self.nest_level -= 1
        self.write("</expression>")
    
    def CompileInteger(self):
        token = self.tokenizer.read_token()
        self.write("<integerConstant> " + str(token.token) + " </integerConstant>")
    
    def CompileString(self):
        token = self.tokenizer.read_token()
        self.write("<stringConstant> " + token.token + " </stringConstant>")
    
    def CompileTerm(self):
        self.write("<term>")
        self.nest_level += 1
        if self.next_token_type_is([TokenType.INTEGER]): # integerConstant
            self.CompileInteger()
        elif self.next_token_type_is([TokenType.STRING]): # stringConstant
            self.CompileString()
        elif self.next_token_is([Tokens.TRUE,Tokens.FALSE,Tokens.NULL,Tokens.THIS]): # keywordConstant
            self.CompileKeyword([Tokens.TRUE,Tokens.FALSE,Tokens.NULL,Tokens.THIS])
        elif self.next_token_type_is([TokenType.IDENTIFIER]): # varName
            self.CompileVarName()
            if self.next_token_is([Tokens.LEFT_BOX_BRACKET]): # varName '[' expression ']'
                self.CompileSymbol([Tokens.LEFT_BOX_BRACKET])
                self.CompileExpression()
                self.CompileSymbol([Tokens.RIGHT_BOX_BRACKET])
            elif self.next_token_is([Tokens.LEFT_ROUND_BRACKET]): # subroutineCall -> subroutineName '(' expressionList ')'
                self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
                self.CompileExpressionList()
                self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
            elif self.next_token_is([Tokens.DOT]):  # subroutineCall -> (className|varName) '.' subroutineName '(' expressionList ')'
                self.CompileSymbol([Tokens.DOT])
                self.CompileSubroutineName()
                self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
                self.CompileExpressionList()
                self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        elif self.next_token_is([Tokens.LEFT_ROUND_BRACKET]): # '(' expression ')'
            self.CompileSymbol([Tokens.LEFT_ROUND_BRACKET])
            self.CompileExpression()
            self.CompileSymbol([Tokens.RIGHT_ROUND_BRACKET])
        elif self.next_token_is([Tokens.MINUS,Tokens.TILDE]):
            self.CompileSymbol([Tokens.MINUS,Tokens.TILDE])
            self.CompileTerm()
        self.nest_level -= 1
        self.write("</term>")
    
    def CompileTermMore(self):
        if self.next_token_is([Tokens.PLUS,Tokens.MINUS,Tokens.MULTI,Tokens.DIV,Tokens.AND,Tokens.PIPE,Tokens.LESS_THAN,Tokens.GREATER_THAN,Tokens.EQUAL]):
            self.CompileSymbol([Tokens.PLUS,Tokens.MINUS,Tokens.MULTI,Tokens.DIV,Tokens.AND,Tokens.PIPE,Tokens.LESS_THAN,Tokens.GREATER_THAN,Tokens.EQUAL])
            self.CompileTerm()
            
    def CompileExpressionList(self):
        self.write("<expressionList>")
        self.nest_level += 1
        if not self.next_token_is([Tokens.RIGHT_ROUND_BRACKET]):
            self.CompileExpression()
            while True:
                if self.next_token_is([Tokens.COMMA]):
                    self.CompileSymbol([Tokens.COMMA])
                    self.CompileExpression()
                else:
                    break
        self.nest_level -= 1
        self.write("</expressionList>")
