#!/usr/bin/env python3
# A trivial programming language compiler
#
# Author: Pedro Reis dos Santos
# Date	: July 28, 2020

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
	print(pf['ADD']%(), file=out)

def b_expr_4(n,pf,out):
	''' expr : ADD(INT,INT) 1 '''
	print(pf['IMM'] % (n.left().value() + n.right().value()), file=out)

goal = 'prog'
import scan, gram
import pyburg.pyburg as pyburg
import pyburg.postfix as postfix
terminals = ('ADD', 'SET', 'PROG', 'DECLS', 'NIL', 'INSTRS', 'EXPR') + tuple(scan.tokens)
lbl = 0

def gen(filename):
	pyburg.run(gram.run(filename))

if __name__ == '__main__':
	from sys import argv, stdout
	if len(argv) > 1:
		tree = gram.run(argv[1])
		print(tree)
		print("AST:", tree)
		if not tree: exit(1)
		out = open(argv[2], 'w') if len(argv) > 2 else stdout
		pyburg.run(tree, user=postfix.x64, output=out)
	else:
		print("USAGE: %s example.snp [out.asm]" % argv[0])
