import ply.lex as lex

reserved = {
	'while' : 'WHILE',
	'if' : 'IF',
	'else' : 'ELSE',
	'print' : 'PRINT',
	'read' : 'READ',
	'program' : 'PROGRAM',
	'end' : 'END',
}

tokens = [ 'VARIABLE', 'STRING', 'INTEGER', 'GE', 'LE', 'EQ', 'NE', ] + list(reserved.values())

literals = "-()<>=+*/%;{}."

# Regular expression rules for simple tokens
t_GE	= r'\>\='
t_LE	= r'\<\='
t_EQ	= r'\=\='
t_NE	= r'\!\='

def t_VARIABLE(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	t.type = reserved.get(t.value,'VARIABLE')
	return t

def t_STRING(t):
	r'\'[^\']*\''
	return t

def t_INTEGER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_COMMENT(t):
	r'\#.*'
	pass # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
	print("line", t.lineno, ": illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def scanner():
	return lex.lex()

def scan(filename):
	with open(filename, 'r') as file:
		data = file.read()
	lexer = lex.lex() # use lex.lex(debug=True) for debug
	lexer.input(data)
	for t in lexer:
		print(t)

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		scan(argv[1])
