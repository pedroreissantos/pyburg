#ENV=PYTHONPATH=.. # uncomment if pyburg is not installed
TST=cmp.spl div.spl ex2.spl ex3.spl ex4.spl ex5.spl ex6.spl ex.spl fib.spl \
	gcd.spl hello.spl printi.spl prio.spl tri.spl x.spl
EXS=$(TST:%.spl=%)
EXE=$(ENV) python3 ../code.py
EXT=.spl
LIB=../../run/librun.a
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
	rm -rf $(EXS) *.asm *.o ../parser.out ../parsetab.py ../__pycache__
