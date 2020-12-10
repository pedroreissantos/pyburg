#!/usr/bin/env python3
# Code generation optimization with two registers
#
# Author: Pedro Reis dos Santos
# Date  : December 8, 2020

# -------------- SCAN ----------------
reserved = {}
tokens = [ 'ID', 'CONST' ]
literals = "+=;"
t_ignore = ' \t' # ignore spaces and tabs
def t_ID(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	t.type = reserved.get(t.value,'ID')
	return t
def t_CONST(t):
	r'\d+'
	t.value = int(t.value)
	return t
def t_COMMENT(t):
	r'\#.*'
	pass # No return value. Token discarded
def t_newline(t): # keep track of line numbers
	r'\n+'
	t.lexer.lineno += len(t.value)
def t_error(t): # Error handling
	print("line", t.lineno, ": illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# -------------- GRAM ----------------
from pyburg.Tree import * # AST
precedence =  [('nonassoc', '='), ('left', '+')]
def p_file_1(p):
	'''file : expr ';' '''
	p[0] = BinNode('END', NilNode('NIL'), p[1])
def p_file_2(p):
	'''file : file expr ';' '''
	p[0] = BinNode('END', p[1], p[2])
def p_expr_1(p):
	'''expr : ID '''
	p[0] = StrNode('ID', p[1])
def p_expr_2(p):
	'''expr : CONST '''
	p[0] = IntNode('CONST', p[1])
def p_expr_3(p):
	'''expr : ID '=' expr '''
	p[0] = BinNode('ASSIGN', StrNode('ID', p[1]), p[3])
def p_expr_4(p):
	'''expr : expr '+' expr '''
	p[0] = BinNode('ADD', p[1], p[3])
def p_error(p):
	print("line", p.lineno, ": syntax error at or before", p.type, "=", p.value)

# -------------- CODE ----------------
reg = 0 # used register
def sameVar(p) : return 1 if p.left().text() == p.right().left().text() else 1000
def otherVar(p) : return 1 if p.left().text() == p.right().right().text() else 1000

def b_file_1(p,user,output):
	''' file : END(file,expr) 0 '''

def b_file_2(p,user,output):
	''' file : NIL 0 '''

def b_expr_1(p,user,output):
	''' expr : ID 1 '''
	global reg
	print("mov r%d, [%s]" % (reg, p.text()), file=output)
	if reg == 0 : reg = 1

def b_expr_2(p,user,output):
	''' expr : CONST 1 '''
	global reg
	print("mov r%d, %d" % (reg, p.value()), file=output)
	if reg == 0 : reg = 1

def b_expr_3(p,user,output):
	''' expr : ASSIGN(ID,expr) 1 '''
	print("mov [%s], r0" % p.left().text(), file=output)

def b_expr_4(p,user,output):
	''' expr : ADD(expr,expr) 1 '''
	print("add r0, r1", file=output)

def b_expr_5(p,user,output):
	''' expr : ADD(expr,CONST) 1 '''
	print("add r0, %d" % p.right().value(), file=output)

def b_expr_6(p,user,output):
	''' expr : ADD(CONST,expr) 1 '''
	print("add r0, %d" % p.left().value(), file=output)

def b_expr_7(p,user,output):
	''' expr : ADD(CONST,CONST) 1 '''
	print("mov r0, %d" % (p.left().value() + p.right().value()), file=output)

def b_expr_8(p,user,output):
	''' expr : ASSIGN(ID,ADD(ID,expr)) sameVar '''
	print("add [%s], r0" % p.left().text(), file=output)

def b_expr_9(p,user,output):
	''' expr : ASSIGN(ID,ADD(expr,ID)) otherVar '''
	print("add [%s], r0" % p.left().text(), file=output)

def b_expr_10(p,user,output):
	''' expr : ASSIGN(ID,ADD(ID,CONST)) sameVar '''
	print("incr [%s], %d" % (p.left().text(), p.right().right().value()), file=output)

def b_expr_11(p,user,output):
	''' expr : ASSIGN(ID,ADD(CONST,ID)) otherVar '''
	print("incr [%s], %d" % (p.left().text(), p.right().left().value()), file=output)

goal = 'file'
terminals = [ 'ASSIGN', 'ADD', 'END', 'NIL' ] + tokens

import ply.lex as lex
import ply.yacc as yacc
from pyburg.pyburg import run

def parse(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return yacc.yacc().parse(data, tracking=True, lexer=lex.lex())

if __name__ == '__main__':
	from sys import argv, stdout
	if len(argv) > 1:
		tree = parse(argv[1])
		print("AST:", tree)
		if not tree: exit(1)
		out = open(argv[2], 'w') if len(argv) > 2 else stdout
		run(tree, output=out)
	else:
		print("USAGE: %s example.ex [out.asm]" % argv[0])
