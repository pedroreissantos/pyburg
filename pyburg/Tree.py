'''This module provides a binary tree representation'''
class Tree:
	'''Tree basic node'''
	def label(self):
		'''each node is identified by a label'''
		return None
	def left(self):
		'''left branch of the binary tree'''
		return None
	def right(self):
		'''right branch of the binary tree'''
		return None
	def __repr__(self):
		repr = "[ label="+str(self.label())
		if self.left():
			repr += ' left=' + self.left().__repr__()
		if self.right():
			repr += ' right=' + self.right().__repr__()
		if getattr(self, 'state', None):
			repr += ' state=' + str(self.state)
		return repr + ']'

class NilNode(Tree):
	'''Tree node without other information other than the operator'''
	def __init__(self,op):
		self.op = op
	def __str__(self):
		return "(" + str(self.op) + ")"
	def label(self):
		return self.op

class IntNode(Tree):
	'''Tree node containing a value'''
	def __init__(self,op,value):
		self.op = op
		self.val = value
	def __str__(self):
		return "(" + str(self.op) + " " + str(self.val) + ")"
	def label(self):
		return self.op
	def value(self):
		return self.val

class StrNode(Tree):
	'''Tree node containing a string text'''
	def __init__(self,op,text):
		self.op = op
		self.txt = text
	def label(self):
		return self.op
	def text(self):
		return self.txt
	def __str__(self):
		return "(" + str(self.op) + " " + self.txt + ")"

class UniNode(Tree):
	'''Tree node containing a single child node'''
	def __init__(self,op,lft):
		self.op = op
		self.lft = lft
	def label(self):
		return self.op
	def left(self):
		return self.lft
	def __str__(self):
		return "(" + str(self.op) + " " + str(self.lft) + ")"

class BinNode(Tree):
	'''Tree node containing two child nodes'''
	def __init__(self,op,lft,rgt):
		self.op = op
		self.lft = lft
		self.rgt = rgt
	def label(self):
		return self.op
	def left(self):
		return self.lft
	def right(self):
		return self.rgt
	def __str__(self):
		return "(" + str(self.op) + " " + str(self.lft) + " " + str(self.rgt) + ")"

#print(BinNode(1,UniNode(2,StrNode(3,"aa")),IntNode(4,12)))
#print(IntNode(7,21).left())
