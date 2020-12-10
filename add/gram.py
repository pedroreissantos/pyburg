import ply.yacc as yacc
from scan import tokens
from pyburg.Tree import * # AST

# -------------- RULES ----------------

precedence = [('left', '+')]

def p_file_1(p):
	'''file : decls '{' instrs '}' '''
	p[0] = BinNode('PROG', p[1], p[3])

def p_decls_1(p):
	'''decls : '''
	p[0] = NilNode('NIL')

def p_decls_2(p):
	'''decls : decls decl'''
	p[0] = BinNode('DECLS', p[1], p[2])

def p_decl_1(p):
	'''decl : ID '=' STR ';' '''
	p[0] = BinNode('SET', StrNode('ID', p[1]), StrNode('STR', p[3]))
	setattr(p[0].left(), 'info', 'STR')
	tabid[p[1]] = 'STR'

def p_decl_2(p):
	'''decl : ID '=' INT ';' '''
	p[0] = BinNode('SET', StrNode('ID', p[1]), IntNode('INT', p[3]))
	setattr(p[0].left(), 'info', 'INT')
	tabid[p[1]] = 'INT'

def p_instrs_1(p):
	'''instrs : '''
	p[0] = NilNode('NIL')

def p_instrs_2(p):
	'''instrs : instrs instr'''
	p[0] = BinNode('INSTRS', p[1], p[2])

def p_instr_1(p):
	'''instr : PRINT strs ';' '''
	p[0] = UniNode('PRINT', p[2])

def p_strs_1(p):
	'''strs : expr'''
	p[0] = p[1]

def p_strs_2(p):
	'''strs : strs ',' expr'''
	p[0] = BinNode('EXPR', p[1], p[3])

def p_expr_1(p):
	'''expr : ID'''
	p[0] = StrNode('ID', p[1])
	setattr(p[0], 'info', tabid[p[1]])

def p_expr_2(p):
	'''expr : INT'''
	p[0] = IntNode('INT', p[1])
	setattr(p[0], 'info', 'INT')

def p_expr_3(p):
	'''expr : expr '+' expr'''
	p[0] = BinNode('ADD', p[1], p[3])
	if p[1].info == 'STR' or p[3].info == 'STR':
		raise RuntimeError("only integers can be added")
	setattr(p[0], 'info', 'INT')

def p_expr_4(p):
	'''expr : STR'''
	p[0] = StrNode('STR', p[1])
	setattr(p[0], 'info', 'STR')

def p_error(p):
	print("line", p.lineno, ": syntax error at or before", p.type, "=", p.value)

tabid={}

# Build the parser
parser = yacc.yacc()

def run(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return parser.parse(data, tracking=True)

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		run(argv[1])
