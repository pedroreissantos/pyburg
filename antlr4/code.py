#!/usr/bin/env python3
# snap programming language compiler
#
# Author: Pedro Reis dos Santos
# Date    : July 8, 2025

from sys import argv, stdout
from Tree import * # AST
from pyburg.pyburg import run
from snapParser import snapParser
from Snap import main

goal = 'prog'
terminals = tuple(snapParser.symbolicNames)
lbl = 0
pic = "" # "@GOTPCREL"

def b_prog_1(node, user, out):
    '''prog: FILE(decls,instrs) 2'''
    print(" xorq %rax, %rax\n ret", file=out)
def b_decls_1(node, user, out):
    '''decls: NIL'''
    print(".extern _println\n.extern _prints\n.extern _printi", file=out)
def b_decls_2(node, user, out):
    '''decls: DECLS(decls, decl)'''
    pass
def b_decl_1(node, user, out):
    '''decl: ASSIGN(ID,STR)'''
    print(".section .rodata\n.align 8\n" + node.left().text() + ": .string " + node.right().text(), file=out)
def b_decl_2(node, user, out):
    '''decl: ASSIGN(ID,INT)'''
    print(".section .data\n.align 8\n" + node.left().text() + ": .quad " + str(node.right().value()), file=out)
def b_instrs_1(node, user, out):
    '''instrs: NIL'''
    print(".section .note.GNU-stack,\"\",@progbits\n.section .text\n.align 8\n .globl _main #:function\n_main:", file=out)
def b_instrs_2(node, user, out):
    '''instrs: SEP(instrs, instr)    '''
    pass # no code between instructions
def b_instr_1(node, user, out):
    '''instr: PRINT(strs)  1'''
    print(" call _println", file=out)
def b_strs_1(node, user, out):
    '''strs: COMMA(strs,str) 2'''
    print(" movq %rax, %rdi\n call _prints", file=out)
def b_strs_2(node, user, out):
    '''strs: COMMA(strs,expr) 2'''
    print(" movq %rax, %rdi\n call _printi", file=out)
def b_strs_3(node, user, out):
    '''strs: str 2'''
    print(" movq %rax, %rdi\n call _prints", file=out)
def b_strs_4(node, user, out):
    '''strs: expr 2'''
    print(" movq %rax, %rdi\n call _printi", file=out)
def b_str_1(node, user, out):
    '''str: ID isSTR'''
    print(" leaq " + node.text() + pic + "(%rip), %rax", file=out)
def b_str_2(node, user, out):
    '''str: STR 1'''
    global lbl
    lbl += 1
    print(".section .rodata\n.align 8\n_" + str(lbl) + ": .string " + node.text() + "\n.section .text\n leaq _" + str(lbl) + pic + "(%rip), %rax", file=out)
def b_expr_1(node, user, out):
    '''expr: ID isINT'''
    print(" movq " + node.text() + pic + "(%rip), %rax", file=out)
def b_expr_2(node, user, out):
    '''expr: INT 1'''
    print(" movq $" + str(node.value()) + ", %rax", file=out)
def b_save_1(node, user, out):
    '''save: expr 1'''
    print(" movq %rax, %rbx", file=out)
def b_expr_3(node, user, out):
    '''expr: ADD(save, expr) 1'''
    print(" addq %rbx, %rax", file=out)
#! optimizations: constant folding and strength reduce
def b_expr_4(node, user, out):
    '''expr: ADD(INT, INT) 1'''
    print(" movq $" + str(node.left().value() + node.right().value()) + ", %rax", file=out)
def b_expr_5(node, user, out):
    '''expr: ADD(expr, INT) 1'''
    print(" addq $" + str(node.right().value()) + ", %rax", file=out)
def b_expr_6(node, user, out):
    '''expr: ADD(INT, expr) 1'''
    print(" addq $" + str(node.left().value()) + ", %rax", file=out)
def isSTR(p) :
    return 1 if p.place() == snapParser.STR else 1000
def isINT(p) :
    return 1 if p.place() == snapParser.INT else 1000

def parse(data, out=stdout):
    tree = main(data)
    print("AST:", tree)
    #if not tree: exit(1)
    run(tree, output=out)

if __name__ == '__main__':
    if len(argv) > 1:
        with open(argv[1]) as fp: data = fp.read()
    else:
        data = input('> ')
    out = open(argv[2], 'w') if len(argv) > 2 else stdout
    parse(data, out)
