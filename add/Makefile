#ENV=PYTHONPATH=.. # uncomment if pyburg is not installed
EXS=hello twelve xy
EXE=$(ENV) python3 code.py
EXT=.snp
LIB=../run/librun.a
.SUFFIXES: .asm $(EXT)

all::
	$(MAKE) $(MFLAGS) -C `dirname $(LIB)`
	for i in $(EXS); do $(MAKE) $(MFLAGS) $$i; done
$(EXT).asm:
	$(EXE) $< $@
.asm.o:
	$(AS) $< -o $@
%: %.o
	$(LD) -o $@ $< $(LIB)
clean::
	rm -rf $(EXS) *.asm *.o parser.out parsetab.py __pycache__
