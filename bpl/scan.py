import ply.lex as lex

reserved = {
	'auto'	: 'AUTO',
	'extrn'	: 'EXTRN',
	'if'	: 'IF',
	'else'	: 'ELSE',
	'while'	: 'WHILE',
	'case'	: 'CASE',
	'default': 'DEFAULT',
	'switch': 'SWITCH',
	'break'	: 'BREAK',
	'goto'	: 'GOTO',
	'return' : 'RETURN',
}

tokens = ['CTE', 'NAME', 'STRING'] + [ 'GE', 'LE', 'EQ', 'NE', 'LSH', 'RSH', 'INC', 'DEC', 'ASSIGN' ] + list(reserved.values())

literals = "-+*/%!&|~^<>()?:;,\[\]{}#"

# Regular expression rules for simple tokens
t_GE	= r'\>\='
t_LE	= r'\<\='
t_EQ	= r'\=\='
t_NE	= r'\!\='
t_LSH	= r"\<\<"
t_RSH	= r"\>\>"
t_INC	= r"\+\+"
t_DEC	= r"\-\-"
t_ASSIGN = r"\="

def t_NAME(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	t.type = reserved.get(t.value,'NAME')
	return t

def t_STRING(t):
	r'\"([^\*\n\"]|(\*.))*\"'
	s = ''
	esc = False
	for ch in t.value[1:-1]:
		if esc:
			esc = False
			if ch == '*' or ch == '(' or ch == ')' or ch == '\'' or ch == '"':
				s += ch
			elif ch == 't': s += '\t'
			elif ch == 'n': s += '\n'
			elif ch == '0': s += '\0'
			else: print('Illegal escape in character literal')
		elif ch == '*': esc = True
		else: s += ch
	t.value = s
	return t

def character(s):
	v = 0
	i = 0
	esc = False
	for ch in s:
		if esc:
			esc = False
			if ch == '*' or ch == '(' or ch == ')' or ch == '\'' or ch == '"':
				val = ord(ch)
			elif ch == 't': val = ord('\t')
			elif ch == 'n': val = ord('\n')
			elif ch == '0': val = ord('\0')
			else: print('Illegal escape in character literal')
		elif ch == '*': esc = True
		else: val = ord(ch)
		if not esc:
			 v = v | (val << (i*8));
			 i = i + 1
	return v

def octal(s):
	v = 0
	for ch in s:
		if ch.isdigit():
			v = v * 8 + ord(ch) - ord('0')
		else:
			print('Illegal character in octal literal')
			break
	return v


def t_CTE(t):
	r'(\d+)|(\'([^\*\n\']|(\*.)){1,4}\')'
	if t.value[0] == '0': t.value = octal(t.value)
	elif t.value[0].isdigit(): t.value = int(t.value)
	else: t.value = character(t.value[1:-1])
	return t

def t_COMMENT(t):
	r'(/\*(.|\n)*?\*/)|(//.*)'
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
