.SUFFIXES: .g4 .brg
ID=Snap
CODE=code
VER=4.13.1
LIB=$(JARS)/antlr-$(VER)-complete.jar
JARS=$(HOME)/.local/lib

CC=gcc -static
CFLAGS=-DUNDERSCORE # precede function names with underscore
PYTHON=python3
JAVA=java

ANTLR4=$(JAVA) -Xmx500M -cp $(LIB) org.antlr.v4.Tool -Dlanguage=Python3

all: snap.g4 Snap.py $(CODE).py Tree.py Makefile
	$(ANTLR4) -visitor snap.g4
	# bug in ANTLR-4.13.1
	sed -e "s/\/\/package/#package/" < snapParser.py > aa; mv aa snapParser.py
	sed -e "s/\/\/package/#package/" < snapLexer.py > aa; mv aa snapLexer.py

test::
	$(PYTHON) $(CODE).py xy.snp xy.s
	$(LINK.c) xy.s libsnp.c -o xy
	./xy

clean::
	rm -rf __pycache__ snap*.py *.tokens *.interp *.asm *.s *.o xy *~
