import ply.lex as lex

reserved = {
	'print' : 'PRINT',
}

tokens = [ 'ID', 'STR', 'INT' ] + list(reserved.values())

literals = "{}+=;,"

def t_ID(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	t.type = reserved.get(t.value,'ID')
	return t

def t_STR(t):
	r'\"[^\"]*\"'
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_COMMENT(t):
	r'\/\/.*'
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

# Build the lexer
lexer = lex.lex() # use lex.lex(debug=True) for debug

def scan(filename):
	with open(filename, 'r') as file:
		data = file.read()
	lexer.input(data)
	for t in lexer:
		print(t)

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		scan(argv[1])
