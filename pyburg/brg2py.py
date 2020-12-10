#!/usr/bin/env python3
# convert burg-grammars into pyburg format
#
# Author: Pedro Reis dos Santos
# Date	: July 28, 2020

from ply import *

# -------------- LEX ----------------
tokens = ( 'LITERAL', 'TERMINAL', 'START', 'PPERCENT', 'ID', 'INCLUDE', 'STRING', 'INT', 'CHAR', 'BLOCK', 'NL' )

states = (('block', 'exclusive'),)

literals = [';', ',', '(', ')', '=', ':']
t_ignore = ' \t'

def t_NL(t):
	r'\n'
	t.lexer.lineno += t.value.count("\n")
	return t

t_TERMINAL = r'%term'
t_START = r'%start'
t_INCLUDE = r'%include'
t_STRING = '\"([^\\\n]|(\\.))*?\"'
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_CHAR = '\'([^\\\n]|(\\.))*?\''
t_INT = r'\d+'

def t_PPERCENT(t):
	r'%%'
	if getattr(t.lexer, "lastsection", 0):
		t.value = t.lexer.lexdata[t.lexpos + 2:]
		t.lexer.lexpos = len(t.lexer.lexdata)
	else:
		t.lexer.lastsection = 0
	return t

def t_ccomment(t):
	r'/\*(.|\n)*?\*/'
	t.lexer.lineno += t.value.count('\n')

t_ignore_cppcomment = r'//.*'
t_ignore_rulecomment = r'%!.*'

def t_LITERAL(t):
	r'%\{(.|\n)*?%\}'
	t.lexer.lineno += t.value.count("\n")
	return t

def t_NEWLINE(t):
	r'\n'
	t.lexer.lineno += 1

def t_block(t):
	r'\{'
	t.lexer.blockstart = t.lexpos
	t.lexer.level = 1
	t.lexer.begin('block')

def t_block_ignore_string(t):
	r'\"([^\\\n]|(\\.))*?\"'

def t_block_ignore_char(t):
	r'\'([^\\\n]|(\\.))*?\''

def t_block_ignore_comment(t):
	r'/\*(.|\n)*?\*/'

def t_block_ignore_cppcom(t):
	r'//.*'

def t_block_lbrace(t):
	r'\{'
	t.lexer.level += 1

def t_block_rbrace(t):
	r'\}'
	t.lexer.level -= 1
	if t.lexer.level == 0:
		t.type = 'BLOCK'
		t.value = t.lexer.lexdata[t.lexer.blockstart:t.lexpos + 1]
		t.lexer.begin('INITIAL')
		t.lexer.lineno += t.value.count('\n')
		return t

t_block_ignore_nonspace = r'[^\s\}\'\"\{]+'
t_block_ignore_whitespace = r'\s+'
t_block_ignore = ""

def t_block_error(t):
	raise RuntimeError

def t_error(t):
	print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
	print(t.value)
	t.lexer.skip(1)

# -------------- YACC ----------------
precedence = []

def p_burg(p):
	'''burg : declsection rulesection'''

def p_declsection(p):
	'''declsection : decls PPERCENT'''
	p.lexer.lastsection = 1

def p_rulesection_1(p):
	'''rulesection : rules PPERCENT'''
	global start
	print('goal = \'{}\''.format(start))
	print('terminals = ', tuple(terms.keys()), ' # + yacc.tokens')
	print('# non-terminals = ', tuple(nts.keys()))
	for line in p[2].splitlines():
		print('# %s' % line)

def p_rulesection_2(p):
	'''rulesection : rules'''

def p_decls_1(p):
	'''decls : '''

def p_decls_2(p):
	'''decls : decls decl'''

def p_decl_1(p):
	'''decl : TERMINAL blist NL'''

def p_decl_2(p):
	'''decl : START nonterm NL'''
	global start
	start = p[2]

def p_decl_3(p):
	'''decl : INCLUDE STRING'''
	print('# include ' + p[2])

def p_decl_4(p):
	'''decl : NL'''

def p_decl_5(p):
	'''decl : error NL'''

def p_decl_6(p):
	'''decl : LITERAL'''
	for line in p[1].splitlines():
		print('# %s' % line)

def p_blist_1(p):
	'''blist : '''

def p_blist_2(p):
	'''blist : blist ID '=' INT'''
	terms[p[2]] = p[4]

def p_blist_3(p):
	'''blist : blist ID '=' CHAR '''
	terms[p[2]] = p[4]

def p_rules_1(p):
	'''rules : '''

def p_rules_2(p):
	'''rules : rules nonterm ':' tree cost block NL'''
	global start
	if not start: start = p[2]
	if p[2] in nts:
		nts[p[2]] = nts[p[2]] + 1
	else:
		nts[p[2]] = 1
	print('def b_%s_%s(n,user,output):\n \'\'\' %s : %s %s \'\'\'' % (p[2], nts[p[2]], p[2], print_tree(p[4]), p[5]))
	for line in p[6].splitlines():
		print(' # %s' % line)
	print()

def p_cost_1(p):
	'''cost : '''
	p[0] = '0'

def p_cost_2(p):
	'''cost : ID'''
	p[0] = p[1]

def p_cost_3(p):
	'''cost : INT'''
	p[0] = str(p[1])

def p_rules_5(p):
	'''rules : rules NL'''
	pass

def p_rules_6(p):
	'''rules : rules error NL'''
	print('error rule')

def p_block_1(p):
	'''block : '''
	p[0] = ''

def p_block_2(p):
	'''block : BLOCK'''
	p[0] = p[1]

def p_nonterm_1(p):
	'''nonterm : ID'''
	p[0] = p[1]

def p_tree_1(p):
	'''tree : ID'''
	p[0] = p[1],

def p_tree_2(p):
	'''tree : ID '(' tree ')' '''
	p[0] = p[1],p[3]

def p_tree_3(p):
	'''tree : ID '(' tree ',' tree ')' '''
	p[0] = p[1],p[3],p[5]

def p_error(p):
	pass
# -------------- main ----------------
start = None
terms = {}
nts = {}

def print_tree(n):
	if len(n) == 1:
		return n[0]
	elif len(n) == 2:
		return n[0] + '(' + print_tree(n[1]) + ')'
	else:
		return n[0] + '(' + print_tree(n[1]) + ',' + print_tree(n[2]) + ')'

def convert(data, debug=False):
	lex.lex()
	yacc.yacc()
	yacc.parse(data, debug)

if __name__ == '__main__':
	from sys import argv
	dbg=False
	if len(argv) > 1 and argv[1] == '-d':
		dbg=True
		argv=argv[1:]
	if len(argv) == 1:
		print('USE: {} filename.brg'.format(argv[0]))
		raise SystemExit
	convert(open(argv[1]).read(), debug=dbg)
