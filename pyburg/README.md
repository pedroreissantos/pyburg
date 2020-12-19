A BURG (Bottom-Up Rewrite Grammar) instruction selection generator compiler

The pyburg/ package includes:
* pyburg.py: instruction selection tool
* brg2py.py: converter from pburg (C, java) to pyburg (python)
* postfix.py: macros for assembly generation: x86, amd64, arm32, ...
* Tree.py: simple binary tree for AST building
* strbuf.py: class to collect output into a string

See https://github.com/pedroreissantos/pyburg for documentation and examples.

@(c) prs, IST 2020
