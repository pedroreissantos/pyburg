#!/usr/bin/env python3
"""
Simple programming language compiler: instruction select and code generation
Author: Pedro Reis dos Santos
Date    : June 28, 2024
"""

import sys
import pyburg
from pyburg.pyburg import run
from pyburg.postfix import pf, x64 # assembler: 'arm','amd64','x64','i386','i386gas','debug','num')
from gram import grammar, tabid
from scan import tokens, scanner

lblcnt=0

def newlbl():
    """ generate a new label """
    global lblcnt
    lblcnt += 1
    return lblcnt

def setlbl(val):
    """ set label to a given value """
    global lblcnt
    lblcnt = val

def mklbl(num):
    """ build a numbered label """
    return "_L"+str(num)

def same_var(node):
    """ compare variables in assignment """
    return 1 if node.left().text() == node.right().left().text() else 1000

def other_var(node):
    """ compare variables in assignment """
    return 1 if node.left().text() == node.right().right().text() else 1000

def b_program(_node,via,out):
    '''program : PROGRAM(list) 0'''
    print(via['RET']+via['DATA'], file=out)
    for var in tabid:
        print((via['LABEL']+via['INTEGER']) % (var, 0), file=out)
    print((via['EXTRN']+via['EXTRN']) % ('_prints', '_println'), file=out)
    print((via['EXTRN']+via['EXTRN']) % ('_printi', '_readi'), file=out)

def b_list_1(_node,via,out):
    '''list : END 0'''
    print((via['TEXT']+via['ALIGN']+via['GLOBL']+via['LABEL']) %
        ('_main', via['FUNC'], '_main'), file=out)

def b_list_2(_node,_via,_out):
    '''list : STMT(list,stmt) 0'''

def b_list_3(_node,_via,_out):
    '''list : stmt 1'''

def b_stmt_1(_node,_via,_out):
    '''stmt : END 0'''

def b_stmt_2(node,via,out):
    '''stmt : STRING 4'''
    lbl = newlbl()
    print((via['RODATA']+via['ALIGN']+via['LABEL']) % mklbl(lbl), file=out)
    for ch_ in node.text().encode('utf-8'):
        print(via['CHAR'] % ch_, file=out)
    print((via['CHAR']+via['TEXT']+via['ADDR']) % (0, mklbl(lbl)), file=out)
    print((via['CALL']+via['CALL']+via['TRASH']) % ('_prints', '_println', via['WORD']), file=out)

def b_stmt_3(_node,via,out):
    '''stmt : PRINT(expr) 3'''
    print((via['CALL']+via['CALL']+via['TRASH']) % ('_printi', '_println', via['WORD']), file=out)
    print((via['EXTRN']+via['EXTRN']) % ('_printi', '_println'), file=out)

def b_stmt_4(node,via,out):
    '''stmt : READ 3'''
    print((via['CALL']+via['PUSH']+via['ADDRA']) % ('_readi', node.text()), file=out)
    print(via['EXTRN'] % '_readi', file=out)

def b_stmt_5(node,via,out):
    '''stmt : ASSIGN(VARIABLE,expr) 1'''
    print(via['ADDRA'] % node.left().text(), file=out)

def b_stmt_6(node,via,out):
    '''stmt : ELSE(if,list) 1'''
    print(via['LABEL'] % mklbl(node.left().place), file=out)

def b_if_1(node,via,out):
    '''if : IF(cond,list) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print((via['JMP']+via['LABEL']) % (mklbl(node.place), mklbl(node.left().place)), file=out)

def b_stmt_7(node,via,out):
    '''stmt : IF(cond,list) 1'''
    print(via['LABEL'] % mklbl(node.left().place), file=out)

def b_cond_1(node,via,out):
    '''cond : expr 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JZ'] % mklbl(node.place), file=out)

def b_stmt_8(node,via,out):
    '''stmt : WHILE(do,list) 1'''
    print((via['JMP']+via['LABEL']) % (mklbl(node.left().left().place),
        mklbl(node.left().place)), file=out)

def b_do_1(node,via,out):
    '''do : DO(begin,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JZ'] % mklbl(lbl), file=out)

def b_begin_1(node,via,out):
    '''begin : START 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['LABEL'] % mklbl(lbl), file=out)

def b_stmt_9(_node,via,out):
    '''stmt : expr 1'''
    print(via['TRASH'] % via['WORD'], file=out)

def b_expr_1(node,via,out):
    '''expr : INTEGER 1'''
    print(via['IMM'] % node.value(), file=out)

def b_expr_2(node,via,out):
    '''expr : VARIABLE 1'''
    print(via['ADDRV'] % node.text(), file=out)

def b_expr_3(_node,via,out):
    '''expr : ADD(expr,expr) 1'''
    print(via['ADD'], file=out)

def b_expr_4(_node,via,out):
    '''expr : SUB(expr,expr) 1'''
    print(via['SUB'], file=out)

def b_expr_5(_node,via,out):
    '''expr : MUL(expr,expr) 1'''
    print(via['MUL'], file=out)

def b_expr_6(_node,via,out):
    '''expr : DIV(expr,expr) 1'''
    print(via['DIV'], file=out)

def b_expr_7(_node,via,out):
    '''expr : MOD(expr,expr) 1'''
    print(via['MOD'], file=out)

def b_expr_8(_node,via,out):
    '''expr : EQ(expr,expr) 1'''
    print(via['EQ'], file=out)

def b_expr_9(_node,via,out):
    '''expr : NE(expr,expr) 1'''
    print(via['NE'], file=out)

def b_expr_10(_node,via,out):
    '''expr : LT(expr,expr) 1'''
    print(via['LT'], file=out)

def b_expr_11(_node,via,out):
    '''expr : LE(expr,expr) 1'''
    print(via['LE'], file=out)

def b_expr_12(_node,via,out):
    '''expr : GT(expr,expr) 1'''
    print(via['GT'], file=out)

def b_expr_13(_node,via,out):
    '''expr : GE(expr,expr) 1'''
    print(via['GE'], file=out)

def b_expr_14(_node,via,out):
    '''expr : UMINUS(expr) 1'''
    print(via['NEG'], file=out)

def b_do_2(node,via,out):
    '''do : DO(begin,LE(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JGT'] % mklbl(lbl), file=out)

def b_do_3(node,via,out):
    '''do : DO(begin,LT(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JGE'] % mklbl(lbl), file=out)

def b_do_4(node,via,out):
    '''do : DO(begin,GE(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JLT'] % mklbl(lbl), file=out)

def b_do_5(node,via,out):
    '''do : DO(begin,GT(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JLE'] % mklbl(lbl), file=out)

def b_do_6(node,via,out):
    '''do : DO(begin,EQ(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JNE'] % mklbl(lbl), file=out)

def b_do_7(node,via,out):
    '''do : DO(begin,NE(expr,expr)) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JEQ'] % mklbl(lbl), file=out)

def b_cond_2(node,via,out):
    '''cond : LE(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JGT'] % mklbl(node.place), file=out)

def b_cond_3(node,via,out):
    '''cond : LT(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JGE'] % mklbl(node.place), file=out)

def b_cond_4(node,via,out):
    '''cond : GE(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JLT'] % mklbl(node.place), file=out)

def b_cond_5(node,via,out):
    '''cond : GT(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JLE'] % mklbl(node.place), file=out)

def b_cond_6(node,via,out):
    '''cond : EQ(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JNE'] % mklbl(node.place), file=out)

def b_cond_7(node,via,out):
    '''cond : NE(expr,expr) 1'''
    lbl = newlbl()
    setattr(node, 'place', lbl)
    print(via['JEQ'] % mklbl(node.place), file=out)

def b_expr_15(node,via,out): # constant folding
    ''' expr : ADD(INTEGER,INTEGER) 1 '''
    print(via['IMM'] % (node.left().value() + node.right().value()), file=out)

def b_expr_16(node,via,out): # strength reduce
    ''' expr : ASSIGN(VARIABLE,ADD(VARIABLE,INTEGER)) same_var '''
    print((via['ADDR']+via['INCR']) % (node.left().text(), node.right().right().value()), file=out)

def b_expr_17(node,via,out): # strength reduce
    ''' expr : ASSIGN(VARIABLE,ADD(INTEGER,VARIABLE)) other_var '''
    print((via['ADRR']+via['INCR']) % (node.left().text(), node.right().left().value()), file=out)

goal = 'program'
terminals =    ( 'IFX', 'UMINUS', 'DO', 'START', 'ASSIGN',
'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'GT', 'LT', 'STMT' )    + tuple(tokens)

def parse(filename):
    """ invoque parser and return abstract syntax tree (AST) """
    with open(filename, 'r', encoding="utf8") as file:
        data = file.read()
    return grammar().parse(data, tracking=True, lexer=scanner())

def gen(filename, module=None, user=x64, output=None):
    """ parse and perform instruction selection """
    ast = parse(filename)
    run(ast, module=module, user=user, output=output)
    setlbl(0)
    return ast

def costs(ast, indent=0, target=None):
    """ print selection costs of an AST """
    print(" " * indent, ast.label(), end=' ')
    if getattr(ast, 'state', None):
        for lhs in ast.state:
            print(lhs + ':' + str(ast.state[lhs][0]), end=' ')
            if target:
                print(ast.state[lhs][1][3].__name__, end=' ')
    print()
    if ast.left():
        costs(ast.left(), indent+1, target)
    if ast.right():
        costs(ast.right(), indent+1, target)

def main(argv):
    """ process command line arguments """
    if len(argv) > 1:
        tree = parse(argv[1])
        if not tree:
            sys.exit(1)
        dbug = 2
        if len(argv) > 4:
            pyburg.debug = dbug = int(argv[4])
        if dbug > 1:
            print("AST:", tree)
        file = open(argv[2], 'w', encoding="utf8") if len(argv) > 2 else sys.stdout
        asm = pf[argv[3]] if len(argv) > 3 else x64
        ret = run(tree, user=asm, output=file)
        if ret == 1:
            costs(tree, 0, True) # print(tree.__repr__())
    else:
        print("USAGE: {argv[0]} example.spl [out.asm [arch [debug-level]]]")
        print("\tarch:", list(pf.keys()))

if __name__ == '__main__':
    main(sys.argv)
