#!/usr/bin/env python3
# A trivial programming language compiler
#
# Author: Pedro Reis dos Santos
# Date	: July 28, 2020

# -------------- SCAN ----------------

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

# -------------- GRAM ----------------

import ply.yacc as yacc
from pyburg.Tree import * # AST

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

# -------------- CODE ----------------

def isSTR(p):
	return 1 if p.info == 'STR' else 1000

def isINT(p):
	return 1 if p.info == 'INT' else 1000

def b_prog_1(n,pf,out):
	''' prog : PROG(decls,instrs) 0 '''
	print((pf['IMM']+pf['POP']+pf['LEAVE']+pf['RET']) % 0, file=out)

def b_decls_1(n,pf,out):
	''' decls : NIL 0 '''
	print((pf['EXTRN']+pf['EXTRN']+pf['EXTRN']) % ("println", "prints", "printi"), file=out)

def b_decls_2(n,pf,out):
	''' decls : DECLS(decls,decl) 0 '''
	# no code between declarations

def b_decl_1(n,pf,out):
	''' decl : SET(ID,STR) 0 '''
	print((pf['TEXT']+pf['ALIGN']+pf['LABEL']+pf['STR']) % (n.left().text(), n.right().text()[1:-1]), file=out)

def b_decl_2(n,pf,out):
	''' decl : SET(ID,INT) 0 '''
	print((pf['TEXT']+pf['ALIGN']+pf['LABEL']+pf['CONST']) % (n.left().text(), n.right().value()), file=out)

def b_instrs_1(n,pf,out):
	''' instrs : NIL 0 '''
	print((pf['TEXT']+pf['ALIGN']+pf['GLOBL']+pf['LABEL']+pf['START']) % ("_main", pf['FUNC'], "_main"), file=out)

def b_instrs_2(n,pf,out):
	''' instrs : INSTRS(instrs,instr) 0 '''
	# no code between instructions

def b_instr_1(n,pf,out):
	''' instr : PRINT(strs) 0 '''
	print(pf['CALL'] % "println", file=out)

def b_strs_1(n,pf,out):
	''' strs : EXPR(strs,str) 0 '''
	print((pf['ARG1']+pf['CALL']+pf['TRASH']) % ("prints", pf['WORD']), file=out)

def b_strs_2(n,pf,out):
	''' strs : EXPR(strs,expr) 0 '''
	print((pf['ARG1']+pf['CALL']+pf['TRASH']) % ("printi", pf['WORD']), file=out)

def b_strs_3(n,pf,out):
	''' strs : str 0 '''
	print((pf['ARG1']+pf['CALL']+pf['TRASH']) % ("prints", pf['WORD']), file=out)

def b_strs_4(n,pf,out):
	''' strs : expr 0 '''
	print((pf['ARG1']+pf['CALL']+pf['TRASH']) % ("printi", pf['WORD']), file=out)

def b_str_1(n,pf,out):
	''' str : ID isSTR '''
	print(pf['ADDR'] % n.text(), file=out)

def b_str_2(n,pf,out):
	''' str : STR 0 '''
	global lbl
	lbl += 1
	print((pf['RODATA']+pf['ALIGN']+pf['LABEL']+pf['STR']+pf['TEXT']+pf['ADDR']) % ( "_L"+str(lbl), n.text()[1:-1], "_L"+str(lbl)), file=out)

def b_expr_1(n,pf,out):
	''' expr : ID isINT '''
	print(pf['ADDRV'] % n.text(), file=out)

def b_expr_2(n,pf,out):
	''' expr : INT 1 '''
	print(pf['IMM'] % n.value(), file=out)

def b_expr_3(n,pf,out):
	''' expr : ADD(expr,expr) 1 '''
	print(pf['ADD'], file=out)

def b_expr_4(n,pf,out):
	''' expr : ADD(INT,INT) 1 '''
	print(pf['IMM'] % (n.left().value() + n.right().value()), file=out)

goal = 'prog'
terminals = ('ADD', 'SET', 'PROG', 'DECLS', 'NIL', 'INSTRS', 'EXPR') + tuple(tokens)
lbl = 0

from pyburg.postfix import arm # produce 'arm' assembler ('amd64','x64','i386','debug','num')
from pyburg.pyburg import run

def parse(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return yacc.yacc().parse(data, tracking=True, lexer=lex.lex())

def gen(filename, module=None, user=arm, output=None):
	pburg.run(parse(filename), module=module, user=user, output=output)

if __name__ == '__main__':
	from sys import argv, stdout
	if len(argv) > 1:
		tree = parse(argv[1])
		print("AST:", tree)
		if not tree: exit(1)
		out = open(argv[2], 'w') if len(argv) > 2 else stdout
		run(tree, user=arm, output=out)
	else:
		print("USAGE: %s example.snp [out.asm]" % argv[0])
