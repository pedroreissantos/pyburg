# tabid in yacc produces LOAD/ADDR for each ID (int:0 func:1 label:2 ptr:3)
# determines ADDR offset and frame size for ENTER

import ply.yacc as yacc
from scan import tokens, scanner
from pyburg.Tree import * # AST

precedence = [
	('nonassoc', 'IFX'),
	('nonassoc', 'ELSE'),
	('right', 'ASSIGN'),
	('right', '?', ':'),
	('left', '|'),
	('left', '^'),
	('left', '&'),
	('left', 'LSH', 'RSH'),
	('nonassoc', 'EQ', 'NE'),
	('nonassoc', '<', '>', 'GE', 'LE'),
	('left', '+', '-'),
	('left', '*', '/', '%'),
	('right', 'INC', 'DEC', 'ADDR', 'UMINUS', '!', '~'),
	('nonassoc', '[', '(')
]

# -------------- RULES ----------------

def p_file_1(p):
	'''file : decl'''
	p[0] = p[1]

def p_decl_1(p):
	'''decl : '''
	p[0] = NilNode('END')

def p_decl_2(p):
	'''decl : decl def'''
	p[0] = BinNode('DECLS', p[1], p[2])

def p_def_1(p):
	'''def : name vc inits ';' '''
	IDnew(p[2].info, p[1].text(), 0)
	p[0] = BinNode('VAR', p[1], BinNode('VC', p[2], p[3]))

def p_def_2(p):
	'''def : name vc ';' '''
	IDnew(p[2].info, p[1].text(), 0)
	p[0] = BinNode('VAR', p[1], BinNode('VC', p[2], NilNode('END')))

def p_def_3(p):
	'''def : _embed0_def names ')' _embed1_def stmt'''
	global pos
	print("# %s: enter %d" % (p[1].text(), -pos))
	gotos()
	IDpop()
	n = BinNode('FARGS', p[1], p[2])
	p[0] = BinNode('FDECL', n, p[5])
	setattr(n, 'enter', -pos)

def p_def_4(p):
	'''def : _embed0_def ')' _embed1_def stmt'''
	global pos
	print("# %s: enter %d" % (p[1].text(), -pos))
	gotos()
	IDpop()
	n = BinNode('FARGS', p[1], NilNode('END'))
	p[0] = BinNode('FDECL', n, p[4])
	setattr(n, 'enter', -pos)

def p__embed0_def(p):
	'''_embed0_def : name '(' '''
	global pos
	IDnew(1, p[1].text(), 0)
	IDpush()
	pos = 8
	p[0] = p[1]

def p__embed1_def(p):
	'''_embed1_def : '''
	global pos
	pos = 0

def p_vc_1(p):
	'''vc : '''
	p[0] = NilNode('END')
	setattr(p[0], 'info', 0)

def p_vc_2(p):
	'''vc : '[' CTE ']' '''
	p[0] = IntNode('DIM', p[2])
	setattr(p[0], 'info', 3)

def p_vc_3(p):
	'''vc : '[' ']' '''
	p[0] = NilNode('DIM')
	setattr(p[0], 'info', 3)

def p_inits_1(p):
	'''inits : ival'''
	p[0] = BinNode('LIST', NilNode('END'), p[1])

def p_inits_2(p):
	'''inits : inits ',' ival'''
	p[0] = BinNode('LIST', p[1], p[3])

def p_names_1(p):
	'''names : name'''
	global pos
	IDnew(0, p[1].text(), pos)
	pos += 4
	p[0] = BinNode('NAMES', NilNode('END'), p[1])

def p_names_2(p):
	'''names : names ',' name'''
	global pos
	IDnew(0, p[3].text(), pos)
	pos += 4
	p[0] = BinNode('NAMES', p[1], p[3])

def p_ival_1(p):
	'''ival : cte'''
	p[0] = p[1]

def p_ival_2(p):
	'''ival : '-' CTE'''
	p[0] = IntNode('CTE', -p[2])

def p_ival_3(p):
	'''ival : name'''
	p[0] = p[1]

def p_cte_1(p):
	'''cte : CTE'''
	p[0] = IntNode('CTE', p[1])

def p_cte_2(p):
	'''cte : STRING'''
	p[0] = StrNode('STRING', p[1])

def p_name_1(p):
	'''name : NAME'''
	p[0] = StrNode('NAME', p[1])

def p_cnames_1(p):
	'''cnames : name vc'''
	p[0] = BinNode('AUTO', NilNode('END'), p[1])
	global pos
	pos -= 4 * dim(p[2])
	IDnew(p[2].info, p[1].text(), pos)

def p_cnames_2(p):
	'''cnames : cnames ',' name vc'''
	p[0] = BinNode('AUTO', p[1], p[3])
	global pos
	pos -= 4 * dim(p[4])
	IDnew(p[4].info, p[3].text(), pos)

def p_enames_1(p):
	'''enames : name'''
	p[0] = BinNode('EXTRN', NilNode('END'), p[1])
	IDnew(0, p[1].text(), 0)
	setattr(p[1], 'info', 0)

def p_enames_2(p):
	'''enames : name '(' ')' '''
	func = StrNode('FUNC', p[1].text())
	p[0] = BinNode('EXTRN', NilNode('END'), func)
	IDnew(1, p[1].text(), 0)
	setattr(func, 'info', 1)

def p_enames_3(p):
	'''enames : enames ',' name'''
	p[0] = BinNode('EXTRN', p[1], p[3])
	IDnew(0, p[3].text(), 0)
	setattr(p[3], 'info', 0)

def p_enames_4(p):
	'''enames : enames ',' name '(' ')' '''
	func = StrNode('FUNC', p[3].text())
	p[0] = BinNode('EXTRN', p[1], func)
	IDnew(1, p[3].text(), 0)
	setattr(func, 'info', 1)

def p_stmt_1(p):
	'''stmt : AUTO cnames ';' stmt'''
	p[0] = BinNode('DECL', p[2], p[4])

def p_stmt_2(p):
	'''stmt : EXTRN enames ';' stmt'''
	p[0] = BinNode('DECL', p[2], p[4])

def p_stmt_3(p):
	'''stmt : _embed0_stmt stmt'''
	p[0] = BinNode('LABEL', p[1], p[2])

def p_stmt_4(p):
	'''stmt : CASE cte ':' stmt'''
	p[0] = BinNode('CASE', swf(p[2]), p[4])

def p_stmt_5(p):
	'''stmt : CASE '-' CTE ':' stmt'''
	p[0] = BinNode('CASE', swf(IntNode('CTE', -p[3])), p[5])

def p_stmt_6(p):
	'''stmt : DEFAULT ':' stmt'''
	p[0] = BinNode('CASE', swf(0), p[3])

def p_stmt_7(p):
	'''stmt : '{' _embed1_stmt stmts '}' '''
	p[0] = UniNode('BLOCK', p[3])
	IDpop()

def p_stmt_8(p):
	'''stmt : IF '(' rvalue ')' stmt %prec IFX'''
	p[0] = BinNode('IF', p[3], p[5])

def p_stmt_9(p):
	'''stmt : IF '(' rvalue ')' stmt ELSE stmt'''
	p[0] = BinNode('ELSE', BinNode('IF', p[3], p[5]), p[7])

def p_stmt_10(p):
	'''stmt : WHILE '(' rvalue ')' stmt'''
	p[0] = BinNode('WHILE', BinNode('DO', NilNode('START'), p[3]), p[5])

def p_stmt_11(p):
	'''stmt : SWITCH '(' rvalue ')' _embed2_stmt stmt'''
	p[0] = BinNode('SWITCH', BinNode('DEFAULT', p[3], swg(1)), p[6])

def p_stmt_12(p):
	'''stmt : BREAK ';' '''
	p[0] = NilNode('BREAK')

def p_stmt_13(p):
	'''stmt : GOTO _embed3_stmt rvalue ';' '''
	p[0] = UniNode('GOTO', p[3])
	global gt
	gt = 0

def p_stmt_14(p):
	'''stmt : RETURN retval ';' '''
	p[0] = UniNode('RETURN', p[2])

def p_stmt_15(p):
	'''stmt : rvalue ';' '''
	p[0] = p[1]

def p_stmt_16(p):
	'''stmt : lvalue '#' rvalue ';' '''
	p[0] = BinNode('ALLOC', p[3], p[1])

def p_stmt_17(p):
	'''stmt : ';' '''
	p[0] = NilNode('END')

def p__embed0_stmt(p):
	'''_embed0_stmt : name ':' '''
	IDinsert(1, 2, p[1].text(), 0)
	p[0] = p[1]

def p__embed1_stmt(p):
	'''_embed1_stmt : '''
	IDpush()

def p__embed2_stmt(p):
	'''_embed2_stmt : '''
	swg(0)

def p__embed3_stmt(p):
	'''_embed3_stmt : '''
	global gt
	gt = 1

def p_stmts_1(p):
	'''stmts : '''
	p[0] = NilNode('END')

def p_stmts_2(p):
	'''stmts : stmts stmt'''
	p[0] = BinNode('STMT', p[1], p[2])

def p_retval_1(p):
	'''retval : '''
	p[0] = IntNode('CTE', 0)

def p_retval_2(p):
	'''retval : '(' rvalue ')' '''
	p[0] = p[2]

def p_lvalue_1(p):
	'''lvalue : name'''
	p[0] = name(p[1])

def p_lvalue_2(p):
	'''lvalue : lvalue '[' rvalue ']' '''
	p[0] = BinNode('INDEX', p[1], p[3])
	setattr(p[0], 'info', 0)

def p_lvalue_3(p):
	'''lvalue : '*' lvalue'''
	p[0] = UniNode('LOAD', p[2])
	setattr(p[0], 'info', 0)

def p_rvalue_1(p):
	'''rvalue : lvalue'''
	p[0] = UniNode('LOAD', p[1])

def p_rvalue_2(p):
	'''rvalue : '(' rvalue ')' '''
	p[0] = p[2]

def p_rvalue_3(p):
	'''rvalue : cte'''
	p[0] = p[1]

def p_rvalue_4(p):
	'''rvalue : rvalue '(' args ')' '''
	p[0] = BinNode('CALL', p[1], p[3])

def p_rvalue_5(p):
	'''rvalue : rvalue '(' ')' '''
	p[0] = BinNode('CALL', p[1], NilNode('END'))

def p_rvalue_6(p):
	'''rvalue : '-' rvalue %prec UMINUS'''
	p[0] = UniNode('UMINUS', p[2])

def p_rvalue_7(p):
	'''rvalue : '!' rvalue'''
	p[0] = UniNode('NOT', p[2])

def p_rvalue_8(p):
	'''rvalue : '&' lvalue %prec ADDR'''
	p[0] = UniNode('PTR', p[2])

def p_rvalue_9(p):
	'''rvalue : '~' rvalue'''
	p[0] = UniNode('BNOT', p[2])

def p_rvalue_10(p):
	'''rvalue : lvalue INC'''
	p[0] = BinNode('INC', p[1], IntNode('CTE', 4 if p[1].info == 3 else 1))

def p_rvalue_11(p):
	'''rvalue : lvalue DEC'''
	p[0] = BinNode('DEC', p[1], IntNode('CTE', 4 if p[1].info == 3 else 1))

def p_rvalue_12(p):
	'''rvalue : INC lvalue'''
	p[0] = BinNode('INC', IntNode('CTE', 4 if p[2].info == 3 else 1), p[2])

def p_rvalue_13(p):
	'''rvalue : DEC lvalue'''
	p[0] = BinNode('DEC', IntNode('CTE', 4 if p[2].info == 3 else 1), p[2])

def p_rvalue_14(p):
	'''rvalue : rvalue '*' rvalue'''
	p[0] = BinNode('MUL', p[1], p[3])

def p_rvalue_15(p):
	'''rvalue : rvalue '/' rvalue'''
	p[0] = BinNode('DIV', p[1], p[3])

def p_rvalue_16(p):
	'''rvalue : rvalue '%' rvalue'''
	p[0] = BinNode('MOD', p[1], p[3])

def p_rvalue_17(p):
	'''rvalue : rvalue '+' rvalue'''
	p[0] = BinNode('ADD', p[1], p[3])

def p_rvalue_18(p):
	'''rvalue : rvalue '-' rvalue'''
	p[0] = BinNode('SUB', p[1], p[3])

def p_rvalue_19(p):
	'''rvalue : rvalue LSH rvalue'''
	p[0] = BinNode('LSH', p[1], p[3])

def p_rvalue_20(p):
	'''rvalue : rvalue RSH rvalue'''
	p[0] = BinNode('RSH', p[1], p[3])

def p_rvalue_21(p):
	'''rvalue : rvalue '<' rvalue'''
	p[0] = BinNode('LT', p[1], p[3])

def p_rvalue_22(p):
	'''rvalue : rvalue '>' rvalue'''
	p[0] = BinNode('GT', p[1], p[3])

def p_rvalue_23(p):
	'''rvalue : rvalue GE rvalue'''
	p[0] = BinNode('GE', p[1], p[3])

def p_rvalue_24(p):
	'''rvalue : rvalue LE rvalue'''
	p[0] = BinNode('LE', p[1], p[3])

def p_rvalue_25(p):
	'''rvalue : rvalue EQ rvalue'''
	p[0] = BinNode('EQ', p[1], p[3])

def p_rvalue_26(p):
	'''rvalue : rvalue NE rvalue'''
	p[0] = BinNode('NE', p[1], p[3])

def p_rvalue_27(p):
	'''rvalue : rvalue '&' rvalue'''
	p[0] = BinNode('BAND', p[1], p[3])

def p_rvalue_28(p):
	'''rvalue : rvalue '^' rvalue'''
	p[0] = BinNode('BXOR', p[1], p[3])

def p_rvalue_29(p):
	'''rvalue : rvalue '|' rvalue'''
	p[0] = BinNode('BOR', p[1], p[3])

def p_rvalue_30(p):
	'''rvalue : rvalue '?' rvalue ':' rvalue'''
	p[0] = BinNode('ARELSE', BinNode('ARIF', p[1], p[3]), p[5])

def p_rvalue_31(p):
	'''rvalue : lvalue ASSIGN rvalue'''
	p[0] = BinNode('ASSIGN', p[3], p[1])

def p_args_1(p):
	'''args : rvalue'''
	p[0] = BinNode('ARG', p[1], NilNode('END'))

def p_args_2(p):
	'''args : args ',' rvalue'''
	p[0] = BinNode('ARG', p[3], p[1])

# -------------- RULES END ----------------

def name(nm):
	global gt, gtr
	if not gt:
		(typ, off) = IDfind(nm.text())
	else: # in a goto statement
		gtr[nm.text()] = (0, 0)
		(typ, off) = IDfind(nm.text(), True)
		if typ < 0:
			typ = 2 # reference to forward label
	# check types
	if off:
		nm = IntNode('LOCAL', off)
	else:
		nm = StrNode('ADDR', nm.text())
	setattr(nm, 'info', typ)
	return nm

def dim(n): return 1 if type(n) == NilNode else n.value()

# goto auxiliar functions
def gotos():
	global gtr, tabid
	for label in gtr:
		if label not in tabid: # tabids[-1] ? IDsearch(label,0,0,1)
			print(label,": undefined")
		else:
			(typ, val) = IDfind(label)
			if typ != 2: print(label, ": nota a label")
	gtr = {}

# switch auxiliar functions

# store case value (or default if val=0) in swr
def swf(val):
	global lbl, swr
	lbl += 1
	lb = "_T"+str(lbl)
	# ensure that it not a duplicate value, and there is no other default
	if not val: # default
		for entry in swr.values():
			if entry[0] == 1:
				print("multiple default")
		swr[lb] = (1, 0)
	else:
		for entry in swr.values():
			if entry[0] == 0 and entry[1] == val.value():
				print("multiple default")
		swr[lb] = (0, val.value())
	return StrNode('NAME', lb)

def swg(pop):
	global swr, swrs
	if not pop:
		swrs += [ swr ]
		swr = {}
		return 0
	n = NilNode('END')
	for label in swr:
		(typ, val) = swr[label]
		if typ != 0:
			n = BinNode('SWITAB', n, UniNode('DEFAULT', StrNode('ETIQ', label)))
		else:
			n = BinNode('SWITAB', n, BinNode('CASE', StrNode('ETIQ', label), IntNode('CTE', val)))
	return n

def p_error(p):
	print("line", p.lineno, ": syntax error at or before", p.type, "=", p.value)

def grammar():
	return yacc.yacc()

def run(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return grammar().parse(data, tracking=True, lexer=scanner())

def IDnew(typ, name, attr):
	global tabid
	tabid[name] = (typ, attr)

def IDfind(name, test=False):
	global tabid, tabids
	if name in tabid: return tabid[name]
	for tab in tabids[::-1]:
		if name in tab: return tab[name]
	print(name, ": undefined")
	return (-1, 0)

def IDinsert(lev, typ, name, attr):
	global tabid, tabids
	if lev > len(tabids): print("Invalid scope level")
	if lev == len(tabids): IDnew(typ, name, attr)
	tabids[-lev][name] = (typ, attr)

def IDsearch(name, skip, lev, test=False):
	global tabid, tabids
	tabs = tabids[::-1] # invert
	for tab in tabs[skip-1:skip+lev]:
		if name in tab: return tab[name]
	if test: print(name, ": undefined")
	return (-1, 0)

def IDpush():
	global tabid, tabids
	tabids += [ tabid ]
	tabid = {}

def IDpop():
	global tabid, tabids
	tabid = tabids[-1]
	tabids = tabids[:-1]

gt = 0
lbl = 0
pos = 0
gtr = {}
swr = {}
swrs = []
tabid = {}
tabids = []

if __name__ == '__main__':
	from sys import argv
	if len(argv) > 1:
		print(run(argv[1]))
