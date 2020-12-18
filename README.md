A BURG (Bottom-Up Rewrite Grammar) instruction selection generator compiler

The pyburg/ package includes:
* pyburg.py: instruction selection tool
* brg2py.py: converter from pburg (C, java) to pyburg (python)
* postfix.py: macros for assembly generation: x86, amd64, arm32, i386, ...
* Tree.py: simple binary tree for AST building
* strbuf.py: class to collect output into a string

Documentation in the docs/ directory:
* pyburg.html: instruction selection with pyburg
* tutorial.html: a complete example
* internals.html: pyburg routine description
* postfix.html: assembly macros description

Code generation examples:
* exs: some demonstration examples
* add: a trivial language implementation
* simple: a simple language implementation
* bpl: B programming language implementation
* run: x64 runtime for the above examples

(C) prs, IST 2020
