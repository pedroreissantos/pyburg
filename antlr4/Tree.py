'''This module provides a binary tree representation'''
class Tree:
    '''Tree basic node'''
    def __init__(self, op, right=None, left=None, value=None, text=None):
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
    def __repr__(self):
        repr = "[ label="+str(self.label())
        if self.lft:
            repr += ' left=' + str(self.lft)
        if self.rgt:
            repr += ' right=' + str(self.rgt)
        if self.val:
            repr += ' value=' + str(self.val)
        if self.txt:
            repr += ' text=' + str(self.txt)
        if self.plc:
            repr += ' place=' + str(self.plc)
        return repr + ']'
