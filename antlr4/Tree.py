'''This module provides a binary tree representation'''
class Tree:
    '''Tree basic node'''
    def __init__(self, op, left=None, right=None, value=None, text=None):
        self.op = op
        self.rgt = right
        self.lft = left
        self.val = value
        self.txt = text
        self.plc = None
    def label(self):
        '''each node is identified by a label'''
        return self.op
    def left(self):
        '''left branch of the binary tree'''
        return self.lft
    def right(self):
        '''right branch of the binary tree'''
        return self.rgt
    def place(self, plc=None):
        '''place holder for tree node'''
        if plc is not None:
            self.plc = plc
        return self.plc
    def value(self):
        return self.val
    def text(self):
        return self.txt
    def string(self, level= 0, labels=None):
        repr = "[ label="+str(self.label())
        if self.lft:
            repr += "\n"+" "*(2*level)
            repr += ' left=' + self.lft.string(level+1)
        if self.rgt:
            repr += "\n"+" "*(2*level)
            repr += ' right=' + self.rgt.string(level+1)
        if labels is not None:
            return repr + "]"
        if self.val:
            repr += ' value=' + str(self.val)
        if self.txt:
            repr += ' text=' + str(self.txt)
        if self.plc:
            repr += ' place=' + str(self.plc)
        return repr + ']'
    def __repr__(self):
        return self.string()
