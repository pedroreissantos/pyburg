"""
Simple programming language compiler: syntactic analysis
Author: Pedro Reis dos Santos
Date    : June 28, 2024
"""
# tabid in yacc produces LOAD/ADDR for each ID (int:0 func:1 label:2 ptr:3)
# determines ADDR offset and frame size for ENTER

from pyburg.Tree import NilNode, UniNode, BinNode, StrNode, IntNode # AST
from ply import yacc
from scan import tokens, scanner # 'tokens' are used by the generator

precedence = [
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('left', '<', '>', 'GE', 'LE', 'EQ', 'NE'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('nonassoc', 'UMINUS')
]

tabid = set()

# -------------- RULES ----------------

def p_program(prd):
    '''program : PROGRAM list END'''
    prd[0] = UniNode('PROGRAM', prd[2])

def p_list_1(prd):
    '''list : stmt'''
    prd[0] = BinNode('STMT', NilNode('END'), prd[1])

def p_list_2(prd):
    '''list : list stmt'''
    prd[0] = BinNode('STMT', prd[1], prd[2])

def p_stmt_1(prd):
    '''stmt : ';' '''
    prd[0] = NilNode('END')

def p_stmt_2(prd):
    '''stmt : PRINT STRING ';' '''
    prd[0] = StrNode('STRING', prd[2])

def p_stmt_3(prd):
    '''stmt : PRINT expr'''
    prd[0] = UniNode('PRINT', prd[2])

def p_stmt_4(prd):
    '''stmt : READ VARIABLE ';' '''
    prd[0] = StrNode('READ', prd[2])
    if prd[2] not in tabid:
        print(f"line {prd.lineno(1)}: unknown variable: {prd[2]}")

def p_stmt_5(prd):
    '''stmt : VARIABLE '=' expr ';' '''
    prd[0] = BinNode('ASSIGN', StrNode('VARIABLE', prd[1]), prd[3])
    tabid.add(prd[1])

def p_stmt_6(prd):
    '''stmt : WHILE '(' expr ')' stmt '''
    prd[0] = BinNode('WHILE', BinNode('DO', NilNode('START'), prd[3]), prd[5])

def p_stmt_7(prd):
    '''stmt : IF '(' expr ')' stmt %prec IFX'''
    prd[0] = BinNode('IF', prd[3], prd[5])

def p_stmt_8(prd):
    '''stmt : IF '(' expr ')' stmt ELSE stmt'''
    prd[0] = BinNode('ELSE', BinNode('IF', prd[3], prd[5]), prd[7])

def p_stmt_9(prd):
    '''stmt : '{' list '}' '''
    prd[0] = prd[2]

def p_expr_1(prd):
    '''expr : INTEGER'''
    prd[0] = IntNode('INTEGER', prd[1])

def p_expr_2(prd):
    '''expr : VARIABLE'''
    prd[0] = StrNode('VARIABLE', prd[1])
    if prd[1] not in tabid:
        print(f"line {prd.lineno(1)}: unknown variable: {prd[1]}")

def p_expr_3(prd):
    '''expr : '-' expr %prec UMINUS'''
    prd[0] = UniNode('UMINUS', prd[2])

def p_expr_4(prd):
    '''expr : expr '+' expr'''
    prd[0] = BinNode('ADD', prd[1], prd[3])

def p_expr_5(prd):
    '''expr : expr '-' expr'''
    prd[0] = BinNode('SUB', prd[1], prd[3])

def p_expr_6(prd):
    '''expr : expr '*' expr'''
    prd[0] = BinNode('MUL', prd[1], prd[3])

def p_expr_7(prd):
    '''expr : expr '/' expr'''
    prd[0] = BinNode('DIV', prd[1], prd[3])

def p_expr_8(prd):
    '''expr : expr '%' expr'''
    prd[0] = BinNode('MOD', prd[1], prd[3])

def p_expr_9(prd):
    '''expr : expr '<' expr'''
    prd[0] = BinNode('LT', prd[1], prd[3])

def p_expr_10(prd):
    '''expr : expr '>' expr'''
    prd[0] = BinNode('GT', prd[1], prd[3])

def p_expr_11(prd):
    '''expr : expr GE expr'''
    prd[0] = BinNode('GE', prd[1], prd[3])

def p_expr_12(prd):
    '''expr : expr LE expr'''
    prd[0] = BinNode('LE', prd[1], prd[3])

def p_expr_13(prd):
    '''expr : expr NE expr'''
    prd[0] = BinNode('NE', prd[1], prd[3])

def p_expr_14(prd):
    '''expr : expr EQ expr'''
    prd[0] = BinNode('EQ', prd[1], prd[3])

def p_expr_15(prd):
    '''expr : '(' expr ')' '''
    prd[0] = prd[2]

# -------------- RULES END ----------------

def p_error(prd):
    """print error message"""
    print(f"line {prd.lineno}: syntax error at or before {prd.type} = {prd.value}")

def grammar():
    """invoque parser"""
    return yacc.yacc()

def run(filename):
    ''' parse a file and print the AST '''
    with open(filename, 'r', encoding='utf8') as file:
        data = file.read()
    return grammar().parse(data, tracking=True, lexer=scanner())

if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        print(run(argv[1]))
