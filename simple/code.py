#!/usr/bin/env python3
# A simple programming language compiler
#
# Author: Pedro Reis dos Santos
# Date	: July 28, 2020

def sameVar(p):
	return 2 if p.left().text() == p.right().left().text() else 1000

def b_stat_1(n, pf, out):
	''' stat : LIST(stat,stat) 0 '''
	print(pf['COMM'] % str(n.lineno), file=out)

def b_stat_2(n, pf, out):
	''' stat : STRING 9 '''
	global lbl
	lbl += 1
	print( (pf['RODATA']+pf['ALIGN']+pf['LABEL']+pf['STR']+pf['TEXT']+pf['ADDR']+pf['CALL']+pf['CALL']+pf['TRASH'] ) % ( "_L"+str(lbl), n.text()[1:-1], "_L"+str(lbl), "_prints", "println", pf['WORD']), file=out)

def b_stat_3(n, pf, out):
	''' stat : PRINT(reg) 3 '''
	print((pf['CALL']+pf['CALL']+pf['TRASH']) % ("_printi", "println", pf['WORD']), file=out)

def b_stat_4(n, pf, out):
	''' stat : READ 1 '''
	print((pf['CALL']+pf['PUSH']+pf['ADDRA']) % ("readi", n.text()), file=out)

def b_stat_9(n, pf, out):
	''' stat : ASSIGN(VARIABLE,reg) 1 '''
	print(pf['ADDRA'] % n.left().text(), file=out)

def b_stat_22(n, pf, out):
	''' stat : reg 1 '''
	print(pf['TRASH'] % pf['WORD'], file=out)

def b_reg_1(n, pf, out):
	''' reg : VARIABLE 1 '''
	print(pf['ADDRV'] % n.text(), file=out)

def b_reg_2(n, pf, out):
	''' reg : INTEGER 1 '''
	print(pf['IMM'] % n.value(), file=out)

def b_reg_3(n, pf, out):
	''' reg : ADD(reg,reg) 1 '''
	print(pf['ADD']%(), file=out)

def b_reg_4(n, pf, out):
	''' reg : SUB(reg,reg) 1 '''
	print(pf['SUB']%(), file=out)

def b_reg_5(n, pf, out):
	''' reg : UMINUS(reg) 1 '''
	print(pf['NEG']%(), file=out)

def b_reg_6(n, pf, out):
	''' reg : MUL(reg,reg) 1 '''
	print(pf['MUL']%(), file=out)

def b_reg_7(n, pf, out):
	''' reg : DIV(reg,reg) 1 '''
	print(pf['DIV']%(), file=out)

def b_reg_8(n, pf, out):
	''' reg : MOD(reg,reg) 1 '''
	print(pf['MOD']%(), file=out)

def b_reg_9(n, pf, out):
	''' reg : EQ(reg,reg) 1 '''
	print(pf['EQ']%(), file=out)

def b_reg_10(n, pf, out):
	''' reg : NE(reg,reg) 1 '''
	print(pf['NE']%(), file=out)

def b_reg_11(n, pf, out):
	''' reg : LT(reg,reg) 1 '''
	print(pf['LT']%(), file=out)

def b_reg_12(n, pf, out):
	''' reg : LE(reg,reg) 1 '''
	print(pf['LE']%(), file=out)

def b_reg_13(n, pf, out):
	''' reg : GE(reg,reg) 1 '''
	print(pf['GE']%(), file=out)

def b_reg_14(n, pf, out):
	''' reg : GT(reg,reg) 1 '''
	print(pf['GT']%(), file=out)

# optimize if both variables are the same (var += cte)
def b_stat_23(n, pf, out):
	''' stat : ASSIGN(VARIABLE,ADD(VARIABLE,INTEGER)) sameVar '''
	print((pf['ADDR']+pf['INCR']) % (n.left().text(), n.right().right().value()), file=out)

def do_lbl(n, opcode, pf, out):
	global lbl
	lbl += 1
	setattr(n,'lbl',"_L"+str(lbl))
	print(pf[opcode] % n.lbl, file=out)

def b_cond_1(n, pf, out):
	''' cond : reg 1 '''
	do_lbl(n, 'JZ', pf, out)

# optimize by combining the 'JZ' with a condition (by negating the condition)
def b_cond_2(n, pf, out):
	''' cond : EQ(reg,reg) 1 '''
	do_lbl(n, 'JNE', pf, out)

def b_cond_3(n, pf, out):
	''' cond : NE(reg,reg) 1 '''
	do_lbl(n, 'JEQ', pf, out)

def b_cond_4(n, pf, out):
	''' cond : GT(reg,reg) 1 '''
	do_lbl(n, 'JLE', pf, out)

def b_cond_5(n, pf, out):
	''' cond : GE(reg,reg) 1 '''
	do_lbl(n, 'JLT', pf, out)

def b_cond_6(n, pf, out):
	''' cond : LT(reg,reg) 1 '''
	do_lbl(n, 'JGE', pf, out)

def b_cond_7(n, pf, out):
	''' cond : LE(reg,reg) 1 '''
	do_lbl(n, 'JGT', pf, out)

def b_stat_24(n, pf, out):
	''' stat : IF(cond,stat) 1 '''
	print(pf['LABEL'] % n.left().lbl, file=out)

def b_if_1(n, pf, out):
	''' if : IF(cond,stat) 1 '''
	global lbl
	lbl += 1
	setattr(n,'lbl',"_L"+str(lbl))
	print((pf['JMP']+pf['LABEL']) % (n.lbl, n.left().lbl), file=out)

def b_stat_25(n, pf, out):
	''' stat : ELSE(if,stat) 1 '''
	print(pf['LABEL'] % n.left().lbl, file=out)

def b_start_1(n, pf, out):
	''' start : START 1 '''
	do_lbl(n, 'LABEL', pf, out)

def b_do_1(n, pf, out):
	''' do : DO(start,reg) 1 '''
	do_lbl(n, 'JZ', pf, out)

def b_do_2(n, pf, out): # use 'cond' optimizations in 'while'
	''' do : DO(start,cond) 0 '''
	setattr(n,'lbl',n.right().lbl) # copy label on right child

def b_stat_26(n, pf, out):
	''' stat : WHILE(do,stat) 1 '''
	print((pf['JMP']+pf['LABEL']) % (n.left().left().lbl, n.left().lbl), file=out)

from gram import grammar, tabid
from scan import scanner, tokens
from pyburg.pyburg import run
from pyburg.postfix import pf, x64

lbl = 0
goal = 'stat'
terminals = ('DIV', 'SUB', 'ASSIGN', 'MUL', 'LT', 'MOD', 'LIST', 'GT', 'ADD', 'UMINUS', 'DO', 'START') + tuple(tokens)

def setup(pf,out):
	print((pf['TEXT']+pf['ALIGN']+pf['GLOBL']+pf['LABEL']+pf['START']) % ("_main", pf['FUNC'], "_main"), file=out)

def wrapup(pf,out):
	print((pf['IMM']+pf['POP']+pf['LEAVE']+pf['RET']+pf['DATA']) % 0, file=out)
	global tabid
	for s in tabid: print((pf['LABEL']+pf['CONST']) % (s, 0), file=out)
	print((pf['EXTRN']+pf['EXTRN']+pf['EXTRN']+pf['EXTRN']) % ("_prints", "_printi", "println", "readi"), file=out)

def parse(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return grammar().parse(data, tracking=True, lexer=scanner())

def gen(filename, module=None, user=x64, output=None):
	setup(user,output)
	ret = run(parse(filename), module=module, user=user, output=output)
	if not ret: wrapup(user,output)

if __name__ == '__main__':
	from sys import argv, stdout
	if len(argv) > 1:
		tree = parse(argv[1])
	if not tree: exit(1)
	print("AST:", tree)
	fp = open(argv[2], 'w') if len(argv) > 2 else stdout
	asm = pf[argv[3]] if len(argv) > 3 else x64
	setup(asm,fp)
	ret = run(tree, user=asm, output=fp)
	if not ret: wrapup(asm,fp)
	else:
		print("USAGE: %s example.spl [out.asm [arch]] " % argv[0])
