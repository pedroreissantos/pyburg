"""
Simple programming language compiler: scanner specification
Author: Pedro Reis dos Santos
Date	: June 28, 2024
"""

from ply import lex

reserved = {
    'if'      : 'IF',
    'else'    : 'ELSE',
    'while'   : 'WHILE',
    'print'   : 'PRINT',
    'read'    : 'READ',
    'program' : 'PROGRAM',
    'end'     : 'END',
}

tokens = ['VARIABLE', 'INTEGER', 'STRING'] + [ 'GE', 'LE', 'EQ', 'NE' ] + list(reserved.values())

literals = r"-()<>=+*/%;{}."

# Regular expression rules for simple tokens
t_GE    = r'\>\='
t_LE    = r'\<\='
t_EQ    = r'\=\='
t_NE    = r'\!\='

def t_VARIABLE(tok):
    r'[A-Za-z][A-Za-z0-9_]*'
    tok.type = reserved.get(tok.value,'VARIABLE')
    return tok

def t_STRING(tok):
    r"'[^']*'"
    tok.value = tok.value[1:-1]
    return tok

def t_INTEGER(tok):
    r'\d+'
    tok.value = int(tok.value)
    return tok

def t_COMMENT(_):
    r'\#.*'
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(tok):
    r'\n+'
    tok.lexer.lineno += len(tok.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(tok):
    """print error message"""
    print(f"line {tok.lineno}: illegal character '{tok.value[0]}'")
    tok.lexer.skip(1)

def scanner():
    ''' invoque scanner '''
    return lex.lex()

def scan(filename):
    ''' scan a file and print the tokens found '''
    with open(filename, 'r', encoding="utf8") as file:
        data = file.read()
    lexer = lex.lex() # use lex.lex(debug=True) for debug
    lexer.input(data)
    for tok in lexer:
        print(tok)

if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        scan(argv[1])
