#! /usr/bin/env python3
from sys import stderr
from pyburg.Tree import *
from pyburg.pyburg import run

global name
global busy

name = [ "eax", "ecx", "edx", "ebx", "esi", "edi", "no-reg" ]
busy= [ 0 ] * len(name)
terms = ( 'ASSIGN', 'CONST', 'VAR', 'PLUS', 'MINUS', 'UMINUS' )

def getReg():
	i = 0
	while i < len(busy) :
		if busy[i] == 0:
			busy[i] = 1
			return i
		i=i+1
	print("out of registers", file=stderr)
	return len(busy) + 1;

def f1(p,u,o):
	print(" mov var, %s"% name[p.right().place])
	busy[p.right().place]=0 # free register child 1

def f2(p, op):
	setattr(p, 'place', p.left().place)
	print(" %s %s, %s"% (op, name[p.place], name[p.right().place]))
	busy[p.right().place]=0

def f3(p, op):
	print(" %s mem, %s"% (op, name[p.left().place]))
	busy[p.left().place]=0

def freg(p):
	setattr(p, 'place', getReg())
	return name[p.place]

def fleft(p):
	setattr(p, 'place', p.left().place)
	return name[p.place]

gram={
"stat:	ASSIGN(VAR,reg) 19":	f1,
"stat:	ASSIGN(VAR,CONST) 20":	lambda p,u,o: print(" mov var, const") ,
"reg:	 mem 18":		lambda p,u,o: print(" mov %s, mem"% freg(p)) ,
"reg:	 VAR 18":		lambda p,u,o: print(" mov %s, var"% freg(p)) ,
"reg:	 CONST 4":		lambda p,u,o: print(" mov %s, const"% freg(p)) ,
"reg:	 PLUS(reg,reg) 3":	lambda p,u,o: f2(p, "add") ,
"reg:	 PLUS(reg,CONST) 4":	lambda p,u,o: print(" add %s, const"% fleft(p)) ,
"reg:	 PLUS(reg,mem) 19":	lambda p,u,o: print(" add %s, mem"% fleft(p)) ,
"reg:	 MINUS(reg,reg) 3":	lambda p,u,o: f2(p, "sub") ,
"reg:	 MINUS(reg,CONST) 4":	lambda p,u,o: print(" sub %s, const"% fleft(p)) ,
"reg:	 MINUS(reg,mem) 19":	lambda p,u,o: print(" sub %s, mem"% fleft(p)) ,
"reg:	 UMINUS(reg) 3":		lambda p,u,o: print(" neg %s"% fleft(p)) ,
"mem:	 reg 19":		lambda p,u,o: f3(p, "mov") ,
"mem:	 CONST 20":		lambda p,u,o: print(" mov mem, const") ,
"mem:	 PLUS(mem,reg) 30":	lambda p,u,o: f3(p, "add") ,
"mem:	 PLUS(mem,CONST) 31":	lambda p,u,o: print(" add mem, const") ,
"mem:	 MINUS(mem,reg) 30":	lambda p,u,o: f3(p, "sub") ,
"mem:	 MINUS(mem,CONST) 31":	lambda p,u,o: print(" sub mem, const") ,
"mem:	 UMINUS(mem) 30":	lambda p,u,o: print(" neg mem"),
"terminals": terms,
"goal": "stat"
}

run(BinNode('ASSIGN',NilNode('VAR'),NilNode('CONST')), gram)
print("***");

run(BinNode('ASSIGN',NilNode('VAR'),NilNode('VAR')), gram)
print("***");

run(BinNode('ASSIGN',NilNode('VAR'),BinNode('PLUS',UniNode('UMINUS',NilNode('VAR')),NilNode('CONST'))), gram)
print("***");

p = BinNode('ASSIGN',
	NilNode('VAR'),
	BinNode('MINUS',
		BinNode('PLUS',
			NilNode('VAR'),
			BinNode('MINUS',
				NilNode('VAR'),
				NilNode('CONST')
			)
		),
		BinNode('PLUS',NilNode('VAR'),NilNode('VAR'))
	)
)
run(p, gram)

print("***")
p = BinNode('MINUS',
	BinNode('PLUS',
		NilNode('VAR'),
		BinNode('MINUS',
			NilNode('VAR'),
			NilNode('CONST')
		)
	),
	BinNode('PLUS',NilNode('VAR'),NilNode('VAR'))
)
run(p, gram)
print('(previous tree does not match a "stat" since the top node (MINUS) only derives a "reg")', file=stderr)
