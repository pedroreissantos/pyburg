# BURG (Bottom-Up Rewrite Grammar) in python
#
# Author: Pedro Reis dos Santos
# Date: July 25, 2020

from ply import *

# -------------- LEX ----------------
tokens = ( 'ID', 'INT', )
literals = [',', '(', ')', ':']
t_ignore = ' \t'
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_INT = r'\d+'

def t_error(t):
	print("%d: Illegal character '%s'" % (t.lexer.lineno, t.value[0]))
	print(t.value)
	t.lexer.skip(1)

# -------------- YACC ----------------
precedence = []
dbg=False

def p_rule_1(p):
	'''rule : ID ':' tree INT'''
	if dbg: print(p[1]+': cost='+p[4])
	p[0] = p[1],p[3],p[4]

def p_rule_2(p):
	'''rule : ID ':' tree'''
	if dbg: print(p[1]+': no cost')
	p[0] = p[1],p[3],0

def p_rule_3(p):
	'''rule : ID ':' tree ID'''
	if dbg: print(p[1]+': Cost='+p[4])
	p[0] = p[1],p[3],p[4]

def p_tree_1(p):
	'''tree : ID'''
	if dbg: print('LEAF='+p[1])
	p[0] = p[1]

def p_tree_2(p):
	'''tree : ID '(' tree ')' '''
	if dbg: print('UNI='+p[1])
	p[0] = p[1],p[3]

def p_tree_3(p):
	'''tree : ID '(' tree ',' tree ')' '''
	if dbg: print('BIN='+p[1])
	p[0] = p[1],p[3],p[5]

def p_error(p):
	print('Rule error:', func)

func=None
rule_parser=None
rule_lexer=None
def rule(name):
	global func, rule_lexer, rule_parser
	if not rule_lexer:
		rule_lexer = lex.lex()
		rule_parser = yacc.yacc(write_tables=False, debug=False)
	func = name.__name__ # for Rule error
	return rule_parser.parse(name.__doc__, lexer=rule_lexer) + ( name, )

import sys

def get_caller_module_dict(levels): # from ply
	''' Return a dictionary containing all the symbols
	defined within a caller further down the call stack. '''
	f = sys._getframe(levels)
	ldict = f.f_globals.copy()
	if f.f_globals != f.f_locals:
		ldict.update(f.f_locals)
	return ldict

def entries(module=None, level=3): # from ply
	''' Get the module dictionary used for the parser '''
	if module:
		_items = [(k, getattr(module, k)) for k in dir(module)]
		fdir = dict(_items)
		# If no __file__ or __package__ attributes are available,
		# try to obtain them from the __module__ instead
		if '__file__' not in fdir:
			fdir['__file__'] = sys.modules[fdir['__module__']].__file__
		if '__package__' not in fdir and '__module__' in fdir:
			if hasattr(sys.modules[fdir['__module__']], '__package__'):
				fdir['__package__'] = sys.modules[fdir['__module__']].__package__
	else:
		fdir = get_caller_module_dict(level) # level=3 inside burg; 2 within burg
	return fdir

def nonterms(gram):
	nts = {}
	for i in gram:
		if i[0] in nts:
			nts[i[0]] = nts[i[0]] + 1
		else:
			nts[i[0]] = 1
	return nts

def cktree(gram, node, nts, terms, visit):
	if type(node) != tuple:
		if node in terms:
			if terms[node] == -1: terms[node] = 1
			if terms[node] != 1:
				print(node, ": inconsistent arity")
				return 1
			return 0
		return ckrules(gram, node, nts, terms, visit)
	if node[0] not in terms:
		print(node[0], ": undefined terminal")
		return 1
	if terms[node[0]] == -1: terms[node[0]] = len(node)
	if terms[node[0]] != len(node):
		print(node[0], ": inconsistent arity")
		return 1
	if len(node) == 2:
		return cktree(gram, node[1], nts, terms, visit)
	if len(node) == 3:
		return cktree(gram, node[1], nts, terms, visit) + cktree(gram, node[2], nts, terms, visit)
	print("UNKNOWN NODE", type(node), node)
	return 1

def ckrules(gram, start, nts, terms, visit):
	if start in visit:
		return 0
	if start not in nts:
		print(start, ": undefined")
		return 1
	ret = 0
	for rule in gram: # find all rules that derive from 'start'
		if rule[0] == start:
			visit[start] = 1
			ret += cktree(gram, rule[1], nts, terms, visit)
	return ret

def ckreach(gram, terminals, start=None):
	if start == None:
		start = gram[0][0]
	nts = nonterms(gram)
	terms = { key: -1 for key in terminals} # terminal's arity
	visit = {}
	ret = ckrules(gram, start, nts, terms, visit)
	for nt in set(nts) - set(visit):
		print(nt+': unreachable')
	return ret + len(set(nts) - set(visit))

def pattern(node, tree, terms):
	if type(tree) != tuple:
		return node.label() == tree or tree not in terms
	if tree[0] not in terms:
		return True
	if node.label() != tree[0]:
		return False
	if len(tree) < 2 or not node.left():
		return False
	if not pattern(node.left(), tree[1], terms):
		return False
	if len(tree) < 3:
		return True
	return node.right() and pattern(node.right(), tree[2], terms)

def match(node, tree, terms):
	if type(tree) != tuple:
		return node.label() == tree and tree in terms
	return pattern(node, tree, terms)

def closure(gram, terms, closures, node, rule, fdir=None):
	if not closures:
		if debug > 4: print("closures")
		for clsr in gram:
			if type(clsr[1]) != tuple and clsr[1] not in terms:
				closures += [ clsr ]
	for clsr in closures:
		if clsr[1] == rule[0]:
			if clsr[2].isnumeric():
				cost = int(clsr[2])
			else:
				cost = fdir[ clsr[2] ](node)
			cost += node.state[rule[0]][0]
			if debug > 3: print("closure: RULE=", clsr, " cost =", cost)
			if clsr[0] not in node.state or cost < node.state[clsr[0]][0]:
				node.state[clsr[0]] = cost,clsr
				closure(gram, terms, closures, node, clsr, fdir)

def sumcosts(node, terms, tree):
	''' sum the costs of all children '''
	if type(tree) != tuple:
		if tree in terms: return 0
		if tree not in node.state:
			if debug > 3: print("***", tree, "***", node, "***", node.state)
			return 1000000
		if debug > 3: print("SUM=",node," COST=",node.state[tree][0])
		return int(node.state[tree][0])
	cost = sumcosts(node.left(), terms, tree[1])
	if len(tree) > 2:
		cost += sumcosts(node.right(), terms, tree[2])
	return cost


# label: each node with the lowest cost for every possible NT
# node: root node of the tree
# gram: BURG grammar (tuple of rules: (NT, pattern, cost, func) )
# terms: list of grammar terminals
# fdir: list of function (for variable cost rules)
# closures: list of closure rules (computed internally)
def label(node, gram, terms, fdir=None, closures=[]):
	if not node: return
	setattr(node, 'state', {})
	label(node.left(), gram, terms, fdir)
	label(node.right(), gram, terms, fdir)
	if debug > 2: print("NODE=", node)
	for rule in gram:
		if match(node, rule[1], terms):
			if rule[2].isnumeric():
				cost = int(rule[2])
			else:
				cost = int(fdir[ rule[2] ](node))
			cost += sumcosts(node, terms, rule[1])
			if debug > 2: print("RULE=", rule, " cost =", cost)
			if rule[0] not in node.state or cost < node.state[rule[0]][0]:
				node.state[rule[0]] = cost,rule
				closure(gram, terms, closures, node, rule, fdir)
	if debug > 2: print("END=", node.state)

# kids: call reduce for each NT in rule
def kids(node, terms, tree, user, output):
	''' find the non-terminal kids of a rule and reduce them '''
	if type(tree) != tuple:
		if tree not in terms:
			reduce(node, terms, tree, user, output)
		return
	kids(node.left(), terms, tree[1], user, output)
	if len(tree) > 2:
		kids(node.right(), terms, tree[2], user, output)

# reduce: call selected functions
# goalnt: the goal NT ('start' for the grammar root)
def reduce(node, terms, goalnt, user, output):
	''' execute a select rule, but first reduce its kids '''
	if debug > 4: print("reduce:",node.label(), node.state)
	if goalnt in node.state:
		rule = node.state[goalnt][1]
		kids(node, terms, rule[1], user, output)
		if debug > 1: print("Reduce:", rule[1], rule[3].__name__, node.state[goalnt][0])
		rule[3](node, user, output)

# user: user defined data (passed to each reduce function
# output: user defined output file (object with .write() method)
def select(tree, gram, terms, start=None, fdir=None, user=None, output=None):
	if not start: start = gram[0][0]
	cnt = ckreach(gram, terms, start)
	if cnt:
		if debug > 0: print(str(cnt)+" errors in grammar")
		return 2
	label(tree, gram, terms, fdir)
	if start not in tree.state or tree.state[start][0] >= 100000:
		if debug > 0: print("No match for start symbol:", start)
		return 1
	if debug > 0: print("Tree selected with cost =", tree.state[start][0])
	reduce(tree, terms, start, user, output)
	return 0

def findterms(node, nts):
	if type(node) != tuple:
		if node not in nts:
			return { node }
		return set({})
	t = { node[0] }
	if len(node) >= 2:
		t.update(findterms(node[1], nts))
	if len(node) >= 3:
		t.update(findterms(node[2], nts))
	return t

def terminals(gram):
	nts = nonterms(gram)
	terms = set()
	for rule in gram:
		terms.update(findterms(rule[1], nts))
	return terms

def table(module = None, level=2):
	fdir = entries(module, level) # list of module function+variables
	table = {}
	for func in fdir:
		if func.startswith('b_'):
			# burg entry: { rule : func }
			table[fdir[func].__doc__] = fdir[func]
		else:
			table[func] = fdir[func] # copy non-burg entries
	return table

# gdir: dict containing grammar entries { rule : func } where
#	rule is 'non_terminal : pattern cost' and func the associated
#	function pointer, or { id : value } for:
#	+ variable cost functions: { func_name : func_pointer }
#	+ terminals list/tuple: { 'terminals' : list_of_names }
#	+ grammar start symbol: { 'goal' : non_terminal }
def parse(gdir):
	global func, rule_lexer, rule_parser
	if not rule_lexer:
		rule_lexer = lex.lex()
		rule_parser = yacc.yacc(write_tables=False, debug=False)
	bnames = [] # list of tuples: (nonterm pattern cost function)
	for name in gdir:
		if name.find(':') >= 0:
			func = name # for Rule error
			bnames += [ rule_parser.parse(name, lexer=rule_lexer) + ( gdir[name], ) ]
	return bnames

# burg: build a BURG grammar (use __doc__ in functions starting with b_)
# fdir: dict of functions (can be obtained with entries(module=None) )
def burg(fdir):
	# from rule import rule
	bnames = [] # list of tuples: (nonterm pattern cost function)
	for func in fdir:
		if func.startswith('b_'):
			bnames += [ rule(fdir[func]) ]
	return bnames

debug = 2 # from 0 (no output) to 5 (highest)

def run(tree, module=None, terms=None, start=None, user=None, output=None):
	if type(module) == dict:
		fdir = module
		gram = parse(fdir)
	else:
		fdir = entries(module) # list of module function+variables
		gram = burg(fdir)
	if not gram:
		if debug > 1: print("No grammar")
		return 3
	if not terms:
		if 'terminals' in fdir:
			terms = fdir['terminals']
		else:
			terms = terminals(gram)
	if not start:
		if 'goal' in fdir:
			start = fdir['goal']
		else:
			if debug > 1: print("No goal")
			return 3
	if not output: output = sys.stdout
	return select(tree, gram, terms, start, fdir, user, output)
