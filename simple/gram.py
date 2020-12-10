import ply.yacc as yacc
from scan import tokens, scanner
from pyburg.Tree import * # AST

precedence = (
	('nonassoc', 'IFX'),
	('nonassoc', 'ELSE'),
	('left', 'GE', 'LE', 'EQ', 'NE', '<', '>'),
	('left', '+', '-'),
	('left', '*', '/', '%'),
	('nonassoc', 'UMINUS'),
)

def p_program(p):
	'program : PROGRAM list END'
	p[0] = p[2]

def p_list(p):
	'list : stmt'
	p[0] = p[1]

def p_liststmt(p):
	'list : list stmt'
	p[0] = BinNode('LIST', p[1], p[2])
	setattr(p[0],'lineno',p.lineno(2))

def p_nilstmt(p):
	'''stmt : ';' '''
	p[0] = NilNode('NIL')

def p_strstmt(p):
	'''stmt : PRINT STRING ';' '''
	p[0] = StrNode('STRING', p[2])

def p_intstmt(p):
	'''stmt : PRINT expr ';' '''
	p[0] = UniNode('PRINT', p[2])

def p_readstmt(p):
	'''stmt : READ VARIABLE ';' '''
	p[0] = StrNode('READ', p[2])
	global tabid
	if p[2] not in tabid: print(p[2], ": undefined")

def p_assignstmt(p):
	'''stmt : VARIABLE '=' expr ';' '''
	p[0] = BinNode('ASSIGN', StrNode('VARIABLE', p[1]), p[3])
	global tabid
	if p[1] not in tabid: tabid += [ p[1] ]

def p_whilestmt(p):
	'''stmt : WHILE '(' expr ')' stmt '''
	p[0] = BinNode('WHILE', BinNode('DO', NilNode('START'), p[3]), p[5])

def p_ifstmt(p):
	'''stmt : IF '(' expr ')' stmt %prec IFX '''
	p[0] = BinNode('IF', p[3], p[5])

def p_ifelsestmt(p):
	'''stmt : IF '(' expr ')' stmt ELSE stmt '''
	p[0] = BinNode('ELSE', BinNode('IF', p[3], p[5]), p[7])

def p_blockstmt(p):
	'''stmt : '{' list '}' '''
	p[0] = p[2]

def p_intexpr(p):
	'expr : INTEGER'
	p[0] = IntNode('INTEGER', p[1])

def p_varexpr(p):
	'expr : VARIABLE'
	p[0] = StrNode('VARIABLE', p[1])
	global tabid
	if p[1] not in tabid: print(p[1], ": undefined")

def p_uminusexpr(p):
	'''expr : '-' expr %prec UMINUS'''
	p[0] = UniNode('UMINUS', p[2])

def p_addexpr(p):
	'''expr : expr '+' expr'''
	p[0] = BinNode('ADD', p[1], p[3])

def p_subexpr(p):
	'''expr : expr '-' expr'''
	p[0] = BinNode('SUB', p[1], p[3])

def p_mulexpr(p):
	'''expr : expr '*' expr'''
	p[0] = BinNode('MUL', p[1], p[3])

def p_divexpr(p):
	'''expr : expr '/' expr'''
	p[0] = BinNode('DIV', p[1], p[3])

def p_modexpr(p):
	'''expr : expr '%' expr'''
	p[0] = BinNode('MOD', p[1], p[3])

def p_ltexpr(p):
	'''expr : expr '<' expr'''
	p[0] = BinNode('LT', p[1], p[3])

def p_gtexpr(p):
	'''expr : expr '>' expr'''
	p[0] = BinNode('GT', p[1], p[3])

def p_geexpr(p):
	'''expr : expr GE expr'''
	p[0] = BinNode('GE', p[1], p[3])

def p_leexpr(p):
	'''expr : expr LE expr'''
	p[0] = BinNode('LE', p[1], p[3])

def p_neexpr(p):
	'''expr : expr NE expr'''
	p[0] = BinNode('NE', p[1], p[3])

def p_eqexpr(p):
	'''expr : expr EQ expr'''
	p[0] = BinNode('EQ', p[1], p[3])

def p_parenexpr(p):
	'''expr : '(' expr ')' '''
	p[0] = p[2]

def p_error(p):
	print("line", p.lineno, ": syntax error at or before", p.type, "=", p.value)

def grammar():
	return yacc.yacc()

def run(filename):
	with open(filename, 'r') as file:
		data = file.read()
	parser = yacc.yacc()
	return parser.parse(data, tracking=True, lexer=scanner())

tabid = []

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		run(argv[1])
