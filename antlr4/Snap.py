# compile: antlr4 -visitor -Dlanguage=Python3 snap.g4
# run: python3 snap xy.snp xy.s
# reis.santos(at)tecnico.ulisboa.pt (C)25jul2025

from antlr4 import *
from snapLexer import snapLexer
from snapParser import snapParser
from Tree import Tree
from sys import argv

class snapVisitor(ParseTreeVisitor):
    symtab = {}
    def add(self, name, typ) :
        self.symtab[name] = typ
    def get(self, name) :
        if name in self.symtab:
            #print("  get", name, self.symtab[name])
            return self.symtab[name]
        raise ValueError(name + ": not found")

    def visitSnap(self, ctx:snapParser.SnapContext):
        ''' Visit a parse tree produced by snapParser#snap.'''
        #print("prs@snap="+ctx.getText()+" #"+str(len(ctx.decl()))+" #"+str(len(ctx.instr())))
        decls = Tree("NIL")
        for i in range(len(ctx.decl())): # -1, -1, -1):
            decls = Tree("DECLS", decls, ctx.decl(i).accept(self))
        instrs = Tree("NIL")
        for i in range(len(ctx.instr())): # -1, -1, -1):
            instrs = Tree("SEP", instrs, ctx.instr(i).accept(self))
        return Tree("FILE", decls, instrs)

    def visitDecl(self, ctx:snapParser.DeclContext):
        ''' Visit a parse tree produced by snapParser#decl.'''
        #print("prs@decl="+ctx.getText(), ctx.ID(), ctx.INT(), ctx.STR())
        self.add(ctx.ID().getText(), "INT" if ctx.INT() else "STR") # add to symbol table with the declared type: INT or STR
        if not ctx.STR():
            return Tree("ASSIGN",
                Tree("ID", text=ctx.ID().getText()),
                Tree("INT", value=int(ctx.INT().getText())))
        return Tree("ASSIGN",
            Tree("ID", text=ctx.ID().getText()),
            Tree("STR", text=ctx.STR().getText()))

    def visitInstr(self, ctx:snapParser.InstrContext):
        ''' Visit a parse tree produced by snapParser#instr.'''
        return Tree("PRINT", ctx.strs().accept(self))

    def visitStrs(self, ctx:snapParser.StrsContext):
        ''' Visit a parse tree produced by snapParser#strs.'''
        #print("prs@strs="+ctx.getText())
        if not ctx.COMMA():
            return ctx.expr().accept(self)
        return Tree("COMMA", ctx.strs().accept(self), ctx.expr().accept(self))

    def visitExpr(self, ctx:snapParser.ExprContext):
        ''' Visit a parse tree produced by snapParser#expr.'''
        #print("prs@expr="+ctx.getText(), ctx.ID(), ctx.INT(), ctx.STR())
        if ctx.ID():
            t = Tree("ID", text=ctx.ID().getText())
            t.place(snapParser.INT if self.get(ctx.ID().getText()) == "INT" else snapParser.STR)
            #print(" ID", t)
            return t
        if ctx.INT():
            t = Tree("INT", value=int(ctx.INT().getText()))
            t.place(snapParser.INT)
            #print(" INT", t)
            return t
        if ctx.STR():
            t = Tree("STR", text=ctx.STR().getText())
            t.place(snapParser.STR)
            #print(" STR", t)
            return t
        t1 = ctx.expr(0).accept(self)
        t2 = ctx.expr(1).accept(self)
        #print(" ADD", t1, t2)
        if t1.place() == snapParser.STR or t2.place() == snapParser.STR:
            raise ValueError("only integers can be added")
        t = Tree("ADD", t1, t2)
        t.place(snapParser.INT)
        return t


def main(data):
    lexer = snapLexer(InputStream(data))
    stream = CommonTokenStream(lexer)
    parser = snapParser(stream)
    return snapVisitor().visit(parser.snap())
    #tree = parser.snap()
    #print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    if len(argv) > 1:
        with open(argv[1]) as fp: data = fp.read()
    else:
        data = input("> ")
    print(main(data))
