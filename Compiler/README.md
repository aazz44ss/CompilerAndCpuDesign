# Compiler

Compile from high-level-language to VM code

	usage:  
		python hl_analyzer.py Square/

	output:  
		xml file that analyze high level language

## High-Level Language Grammar

### Lexical elements (Tokens)

		keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 'static' |  
			'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' | 'false' | 'null' |  
			'this' | 'let' | 'do' | 'if' | 'else' | 'while' | 'return'  
		symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | '-' | '*' |  
			'/' | '&' | '|' | '<' | '>' | '=' | '~'  
	intergerConstant: 0~32767  
	  stringConstant: a string ( not include double quote or newline)  
	     indentifier: a sequence of letters, digits, and underscore('_') not starting with digit  
	     

### Program structure

	class:          'class' className '{' classVarDec* subroutineDec* '}'  
	classVarDec:    ('static' | 'field') type varName (',' varName)* ';'  
	type:           'int' | 'char' | 'boolean' | className  
	subroutineDec:  ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody  
	parameterList:  ((type varName) (','type varName)*)?  
	subroutineBody: '{' varDec* statements '}'  
	varDec:         'var' type varName (',' varName)* ';'  
	className:      identifier  
	subroutineName: identifier  
	varName:        identifier  

### Statements

	statements:      statement*
	statement:       letStatement | ifStatement | whileStatement | doStatement | returnStatement
	letStatement:    'let' varName ('[' expression ']')? '=' expression ';'
	ifStatement:     'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
	whileStatement:  'while' '(' expression ')' '{' statements '}'
	doStatement:     'do' subroutineCall ';'
	returnStatement: 'return' (expression)? ';'

### Expressions

	expression:     term (op term)*
	term:           integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
	subroutineCall: (subroutineName '(' expressionList ')') | ((className|varName) '.' subroutineName '(' expressionList ')')
	expressionList: (expression (',' expression)*)?
	op:             '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
	unaryOp:        '-' | '~'
	keywordConstant:'true' | 'false' | 'null' | 'this'

#### Note

Most of grammer is LL(1), can be parse withou backtracking,
However, when current token is varName, it can be fisrt token in followings:
1. foo
2. foo[expression]
3. foo.bar(expression)
4. foo(expression)
the grammer becomes LL(2).