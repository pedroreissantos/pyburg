#!/usr/bin/env python3
# B programming language compiler
#
# Author: Pedro Reis dos Santos
# Date	: July 28, 2020

from gram import run, grammar
from scan import tokens, scanner
from pyburg.Tree import * # AST
from pyburg.pyburg import run
from pyburg.postfix import pf, x64 # assembler: 'arm','amd64','x64','i386','i386gas','debug','num')

extrns=[] # emit externs at the end only
brklbl=[]
lbl=0

def mklbl(lbl): return "_L"+str(lbl)
def mkfunc(name): return "_"+name
def doasm(p): return 0 if p.left().left().text() == "asm" else 1000

def b_file_1(n,pf,out):
	'''file : decls 0'''
	for ext in extrns: print(pf['EXTRN'] % ext, file=out)

def b_decls_1(n,pf,out):
	'''decls : END 0'''

def b_decls_2(n,pf,out):
	'''decls : DECLS(decls,var) 0'''

def b_decls_3(n,pf,out):
	'''decls : DECLS(decls,func) 0'''

def b_var_1(n,pf,out):
	'''var : VAR 0'''
	variable(n,pf,out)

def b_func_1(n,pf,out):
	'''func : FDECL(fargs,stmt) 0'''
	global extrns
	print((pf['LEAVE']+pf['RET'])%(), file=out); # just in case ...

def b_fargs_1(n,pf,out):
	'''fargs : FARGS 0'''
	name = mkfunc(n.left().text())
	if name in extrns: extrns.remove(name)
	print((pf['TEXT']+pf['ALIGN']+pf['GLOBL']+pf['LABEL']+pf['ENTER']) % (name, pf['FUNC'], name, n.enter * (int(pf['WORD'])/4)), file=out)

def b_stmt_1(n,pf,out):
	'''stmt : BLOCK(stmts) 0'''

def b_stmt_2(n,pf,out):
	'''stmt : DECL(decl,stmt) 0'''

def b_decl_1(n,pf,out):
	'''decl : AUTO 0'''

def b_decl_2(n,pf,out):
	'''decl : EXTRN(decl,extname) 0'''

def b_decl_3(n,pf,out):
	'''decl : END 0'''

def b_stmts_1(n,pf,out):
	'''stmts : END 0'''

def b_stmts_2(n,pf,out):
	'''stmts : STMT(stmts,stmt) 0'''

def b_extname_1(n,pf,out):
	'''extname : NAME 0'''
	global extrns
	extrns += [ n.text() ]

def b_extname_2(n,pf,out):
	'''extname : FUNC 0'''
	global extrns
	extrns += [ mkfunc(n.text()) ]

def b_stmt_3(n,pf,out):
	'''stmt : expr 1'''
	print(pf['TRASH'] % pf['WORD'], file=out)

def b_stmt_4(n,pf,out):
	'''stmt : RETURN(expr) 1'''
	print((pf['POP']+pf['LEAVE']+pf['RET'])%(), file=out)

def b_stmt_5(n,pf,out):
	'''stmt : END 0'''

def b_stmt_6(n,pf,out):
	'''stmt : CALL(LOAD(ADDR),ARG(STRING,END)) doasm'''
	print(n.right().left().text(), file=out)

def b_expr_1(n,pf,out):
	'''expr : CALL(LOAD(ADDR),args) 1'''
	print((pf['CALL']+pf['TRASH']+pf['PUSH']) % (mkfunc(n.left().left().text()), pf['WORD']*n.right().place), file=out)

def b_args_1(n,pf,out):
	'''args : ARG(arg,args) 0'''
	setattr(n, 'place', n.left().place + n.right().place)

def b_args_2(n,pf,out):
	'''args : END 0'''
	setattr(n, 'place', 0)

def b_arg_1(n,pf,out):
	'''arg : expr 1'''
	setattr(n, 'place', 1)

def b_expr_2(n,pf,out):
	'''expr : CTE 1'''
	print(pf['IMM'] % n.value(), file=out)

def b_expr_3(n,pf,out):
	'''expr : STRING 1'''
	global lbl
	lbl += 1
	print((pf['RODATA']+pf['ALIGN']+pf['LABEL']) % mklbl(lbl), file=out)
	for ch in n.text().encode('utf-8'): print(pf['CHAR'] % ch, file=out)
	print((pf['CHAR']+pf['TEXT']+pf['ADDR']) % (0, mklbl(lbl)), file=out)

def b_expr_4(n,pf,out):
	'''expr : ADD(expr,expr) 1'''
	print(pf['ADD']%(), file=out)

def b_expr_5(n,pf,out):
	'''expr : SUB(expr,expr) 1'''
	print(pf['SUB']%(), file=out)

def b_expr_6(n,pf,out):
	'''expr : MUL(expr,expr) 1'''
	print(pf['MUL']%(), file=out)

def b_expr_7(n,pf,out):
	'''expr : DIV(expr,expr) 1'''
	print(pf['DIV']%(), file=out)

def b_expr_8(n,pf,out):
	'''expr : MOD(expr,expr) 1'''
	print(pf['MOD']%(), file=out)

def b_expr_9(n,pf,out):
	'''expr : BOR(expr,expr) 1'''
	print(pf['OR']%(), file=out)

def b_expr_10(n,pf,out):
	'''expr : BXOR(expr,expr) 1'''
	print(pf['XOR']%(), file=out)

def b_expr_11(n,pf,out):
	'''expr : BAND(expr,expr) 1'''
	print(pf['AND']%(), file=out)

def b_expr_12(n,pf,out):
	'''expr : LSH(expr,expr) 1'''
	print(pf['SHTL']%(), file=out)

def b_expr_13(n,pf,out):
	'''expr : RSH(expr,expr) 1'''
	print(pf['SHTRS']%(), file=out)

def b_expr_14(n,pf,out):
	'''expr : EQ(expr,expr) 1'''
	print(pf['EQ']%(), file=out)

def b_expr_15(n,pf,out):
	'''expr : NE(expr,expr) 1'''
	print(pf['NE']%(), file=out)

def b_expr_16(n,pf,out):
	'''expr : LT(expr,expr) 1'''
	print(pf['LT']%(), file=out)

def b_expr_17(n,pf,out):
	'''expr : LE(expr,expr) 1'''
	print(pf['LE']%(), file=out)

def b_expr_18(n,pf,out):
	'''expr : GT(expr,expr) 1'''
	print(pf['GT']%(), file=out)

def b_expr_19(n,pf,out):
	'''expr : GE(expr,expr) 1'''
	print(pf['GE']%(), file=out)

def b_expr_20(n,pf,out):
	'''expr : UMINUS(expr) 1'''
	print(pf['NEG']%(), file=out)

def b_expr_21(n,pf,out):
	'''expr : NOT(expr) 1'''
	print((pf['IMM']+pf['EQ']) % 0, file=out)

def b_expr_22(n,pf,out):
	'''expr : BNOT(expr) 1'''
	print(pf['NOT']%(), file=out)

def b_expr_23(n,pf,out):
	'''expr : AND(and,expr) 1'''
	print(pf['LABEL'] % mklbl(n.left().place), file=out)

def b_and_1(n,pf,out):
	'''and : expr 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print((pf['COPY']+pf['JZ']+pf['TRASH']) % (mklbl(n.place), pf['WORD']), file=out)

def b_expr_24(n,pf,out):
	'''expr : OR(or,expr) 1'''
	print(pf['LABEL'] % mklbl(n.left().place), file=out)

def b_or_1(n,pf,out):
	'''or : expr 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print((pf['COPY']+pf['JNZ']+pf['TRASH']) % (mklbl(n.place), pf['WORD']), file=out)

def b_stmt_7(n,pf,out):
	'''stmt : ELSE(if,stmt) 1'''
	print(pf['LABEL'] % mklbl(n.left().place), file=out)

def b_if_1(n,pf,out):
	'''if : IF(cond,stmt) 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print((pf['JMP']+pf['LABEL']) % (mklbl(n.place), mklbl(n.left().place)), file=out)

def b_stmt_8(n,pf,out):
	'''stmt : IF(cond,stmt) 1'''
	print(pf['LABEL'] % mklbl(n.left().place), file=out)

def b_cond_1(n,pf,out):
	'''cond : expr 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JZ'] % mklbl(n.place), file=out)

def b_expr_25(n,pf,out):
	'''expr : ARELSE(arif,expr) 1'''
	print(pf['LABEL'] % mklbl(n.left().place), file=out)

def b_arif_1(n,pf,out):
	'''arif : ARIF(cond,expr) 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print((pf['JMP']+pf['LABEL']) % (mklbl(n.place), mklbl(n.left().place)), file=out)

def b_stmt_9(n,pf,out):
	'''stmt : WHILE(do,stmt) 1'''
	global brklbl
	brklbl = brklbl[:-1]
	print((pf['JMP']+pf['LABEL']) % (mklbl(n.left().left().place), mklbl(n.left().place)), file=out)

def b_do_1(n,pf,out):
	'''do : DO(begin,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JZ'] % mklbl(lbl), file=out)

def b_begin_1(n,pf,out):
	'''begin : START 1'''
	global lbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['LABEL'] % mklbl(lbl), file=out)

def b_lval_1(n,pf,out):
	'''lval : LOCAL 1'''
	print(pf['LOCAL'] % (n.value() * (pf['WORD']/4)), file=out)

def b_lval_2(n,pf,out):
	'''lval : ADDR 1'''
	print(pf['ADDR'] % n.text(), file=out)

def b_lval_3(n,pf,out):
	'''lval : LOAD(lval) 1'''
	print(pf['LOAD']%(), file=out)

def b_lvec_1(n,pf,out):
	'''lvec : lval 1'''
	print(pf['LOAD']%(), file=out)

def b_lval_4(n,pf,out):
	'''lval : INDEX(lvec,expr) 1'''
	print((pf['IMM']+pf['MUL']+pf['ADD']) % pf['WORD'], file=out)

def b_expr_26(n,pf,out):
	'''expr : LOAD(lval) 1'''
	print(pf['LOAD']%(), file=out)

def b_expr_27(n,pf,out):
	'''expr : PTR(lval) 0'''
	# No code, but keep PTR to avoid missing LOADs

def b_expr_28(n,pf,out):
	'''expr : INC(CTE,lval) 1'''
	print((pf['COPY']+pf['INCR']+pf['LOAD']) % n.left().value(), file=out)

def b_expr_29(n,pf,out):
	'''expr : DEC(CTE,lval) 1'''
	print((pf['COPY']+pf['DECR']+pf['LOAD']) % n.left().value(), file=out)

def b_expr_30(n,pf,out):
	'''expr : INC(lval,CTE) 1'''
	print((pf['COPY']+pf['LOAD']+pf['SWAP']+pf['INCR']) % n.right().value(), file=out)

def b_expr_31(n,pf,out):
	'''expr : DEC(lval,CTE) 1'''
	print((pf['COPY']+pf['LOAD']+pf['SWAP']+pf['DECR']) % n.right().value(), file=out)

def b_assign_1(n,pf,out):
	'''assign : expr 1'''
	print(pf['COPY']%(), file=out)

def b_expr_32(n,pf,out):
	'''expr : ASSIGN(assign,lval) 1'''
	print(pf['STORE']%(), file=out)

def b_expr_33(n,pf,out):
	'''expr : ASSIGN(expr,LOCAL) 1'''
	print((pf['COPY']+pf['LOCA']) % (n.right().value() * (int(pf['WORD'])/4)), file=out)

def b_expr_34(n,pf,out):
	'''expr : ASSIGN(expr,ADDR) 1'''
	print((pf['COPY']+pf['ADDRA']) % n.right().text(), file=out)

def b_expr_35(n,pf,out):
	'''expr : ADDR 1'''
	print(pf['ADDRV'] % n.text(), file=out)

def b_stmt_10(n,pf,out):
	'''stmt : ALLOC(alloc,lval) 1'''
	print(pf['STORE']%(), file=out)

def b_alloc_1(n,pf,out):
	'''alloc : expr 1'''
	print((pf['IMM']+pf['MUL']+pf['ALLOC']+pf['SP']) % pf['WORD'], file=out)

def b_stmt_11(n,pf,out):
	'''stmt : GOTO(expr) 1'''
	print(pf['BRANCH']%(), file=out)

def b_stmt_12(n,pf,out):
	'''stmt : GOTO(LOAD(ADDR)) 1'''
	print(pf['JMP'] % n.left().left().text(), file=out)

def b_name_1(n,pf,out):
	'''name : NAME 1'''
	print(pf['LABEL'] % n.text(), file=out)

def b_stmt_13(n,pf,out):
	'''stmt : LABEL(name,stmt) 0'''

def b_stmt_14(n,pf,out):
	'''stmt : CASE(name,stmt) 0'''

def b_stmt_15(n,pf,out):
	'''stmt : SWITCH(def,stmt) 1'''
	global brklbl
	place = n.left().place
	if place > 0: print(pf['LABEL'] % mklbl(place), file=out)
	print((pf['LABEL']+pf['TRASH']) % (mklbl(brklbl[-1]), pf['WORD']), file=out)
	brklbl = brklbl[:-1]

def b_def_1(n,pf,out):
	'''def : DEFAULT(expr) 0'''
	setattr(n, 'place', swif(n.right(), 0.5, pf, out))
	global lbl, brklbl
	lbl += 1
	brklbl += [ lbl ]

def b_stmt_16(n,pf,out):
	'''stmt : BREAK 1'''
	global brklbl
	print(pf['JMP'] % mklbl(brklbl[-1]), file=out)

def b_stmt_17(n,pf,out):
	'''stmt : CALL(LOAD(ADDR),args) 1'''
	print(pf['CALL'] % mkfunc(n.left().left().text()), file=out)
	if n.right().place: print(pf['TRASH'] % (pf['WORD']*n.right().place), file=out)

def b_stmt_18(n,pf,out):
	'''stmt : INC(CTE,lval) 1'''
	print(pf['INCR'] % n.left().value(), file=out)

def b_stmt_19(n,pf,out):
	'''stmt : DEC(CTE,lval) 1'''
	print(pf['DECR'] % n.left().value(), file=out)

def b_stmt_20(n,pf,out):
	'''stmt : INC(lval,CTE) 1'''
	print(pf['INCR'] % n.right().value(), file=out)

def b_stmt_21(n,pf,out):
	'''stmt : DEC(lval,CTE) 1'''
	print(pf['DECR'] % n.right().value(), file=out)

def b_do_2(n,pf,out):
	'''do : DO(begin,LE(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JGT'] % mklbl(lbl), file=out)

def b_do_3(n,pf,out):
	'''do : DO(begin,LT(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JGE'] % mklbl(lbl), file=out)

def b_do_4(n,pf,out):
	'''do : DO(begin,GE(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JLT'] % mklbl(lbl), file=out)

def b_do_5(n,pf,out):
	'''do : DO(begin,GT(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JLE'] % mklbl(lbl), file=out)

def b_do_6(n,pf,out):
	'''do : DO(begin,EQ(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JNE'] % mklbl(lbl), file=out)

def b_do_7(n,pf,out):
	'''do : DO(begin,NE(expr,expr)) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	brklbl += [ lbl ]
	print(pf['JEQ'] % mklbl(lbl), file=out)

def b_cond_2(n,pf,out):
	'''cond : LE(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JGT'] % mklbl(n.place), file=out)

def b_cond_3(n,pf,out):
	'''cond : LT(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JGE'] % mklbl(n.place), file=out)

def b_cond_4(n,pf,out):
	'''cond : GE(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JLT'] % mklbl(n.place), file=out)

def b_cond_5(n,pf,out):
	'''cond : GT(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JLE'] % mklbl(n.place), file=out)

def b_cond_6(n,pf,out):
	'''cond : EQ(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JNE'] % mklbl(n.place), file=out)

def b_cond_7(n,pf,out):
	'''cond : NE(expr,expr) 1'''
	global lbl, brklbl
	lbl += 1
	setattr(n, 'place', lbl)
	print(pf['JEQ'] % mklbl(n.place), file=out)

goal = 'file'
terminals =	( 'SWITAB', 'IFX', 'ADDR', 'DECLS', 'VAR', 'VC', 'NAMES',
'UMINUS', 'LOAD', 'LABEL', 'END', 'DO', 'START', 'DIM', 'LOCAL', 'PTR',
'DECL', 'AND', 'OR', 'ARG', 'ID', 'ETIQ', 'ADD', 'SUB', 'MUL', 'DIV',
'MOD', 'NOT', 'BOR', 'BXOR', 'BAND', 'LT', 'GT', 'LIST', 'STMT',
'BLOCK', 'ALLOC', 'INDEX', 'CALL', 'ARIF', 'ARELSE', 'BNOT', 'FUNC',
'FDECL', 'FARGS' )	+ tuple(tokens)
# non-terminals =	('assign', 'or', 'def', 'decl', 'stmts', 'args', 'if', 'arg', 'extname', 'alloc', 'lval', 'arif', 'stmt', 'do', 'and', 'lvec', 'expr', 'begin', 'name', 'cond')

def varinit(init, siz, pf, out):
	global lbl
	if init.label() == 'END': return siz
	siz = varinit(init.left(), siz, pf, out)
	var = init.right()
	siz -= 1
	if var.label() == 'CTE':
		print(pf['CONST'] % var.value(), file=out)
	if var.label() == 'NAME':
		print(pf['ID'] % var.text(), file=out)
	if var.label() == 'STRING':
		lbl += 1
		l = mklbl(lbl)
		print((pf['RODATA']+pf['ALIGN']+pf['LABEL']) % l, file=out)
		for ch in var.text().encode('utf-8'): print(pf['CHAR'] % ch, file=out)
		print((pf['CHAR']+pf['DATA']+pf['ID']) % (0, l), file=out)
	return siz

def variable(n, pf, out):
	global lbl
	name = n.left().text()
	vc = n.right().left()
	if name in extrns: extrns.remove(name)
	print((pf['GLOBL']+pf['DATA']+pf['ALIGN']+pf['LABEL']) % (name, pf['OBJ'], name), file=out)
	siz = 1
	if type(vc) == IntNode: siz = vc.value()
	if vc.label() == 'DIM':
		lbl += 1
		print((pf['ID']+pf['LABEL']) % (mklbl(lbl), mklbl(lbl)), file=out);
	siz = varinit(n.right().right(), siz, pf, out)
	if siz > 0: print(pf['BYTE'] % (pf['WORD'] * siz), file=out)

notab = False
def swif(p, dens, pf, out):
	global lbl
	if notab: switab(p, dens)
	x = p
	while p.label() == 'SWITAB':
		n = p.right()
		p = p.left()
		if n.label() == 'CASE':
			print((pf['COPY']+pf['IMM']+pf['JEQ']) % (n.right().value(), n.left().text()), file=out)
	while x.label() == 'SWITAB':
		n = x.right()
		x = x.left()
		if n.label() == 'DEFAULT':
			print(pf['JMP'] % n.left().text(), file=out)
			return -1
	lbl += 1
	print(pf['JMP'] % mklbl(lbl), file=out)
	return lbl

# switch using trees and computed jmps: to be implemented
def switab(p, dens): pass

def parse(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return grammar().parse(data, tracking=True, lexer=scanner())

def gen(filename, module=None, user=x64, output=None):
	run(parse(filename), module=module, user=user, output=output)
	global extrns, brklbl, lbl
	extrns, brklbl, lbl = [], [], 0

if __name__ == '__main__':
	from sys import argv, stdout
	if len(argv) > 1:
		tree = parse(argv[1])
		if not tree: exit(1)
		dbug = 2
		if len(argv) > 4:
			import pyburg
			pyburg.debug = dbug = int(argv[4])
		if dbug > 1: print("AST:", tree)
		fp = open(argv[2], 'w') if len(argv) > 2 else stdout
		asm = pf[argv[3]] if len(argv) > 3 else x64
		run(tree, user=asm, output=fp)
	else:
		print("USAGE: %s example.b [out.asm [arch [debug-level]]]" % argv[0])
