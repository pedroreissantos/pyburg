EXT=.spl
EXE=python3 ../code.py
ARCH=x64
DEBUG=
LIB=../librun.a
AS=as
LD=ld

.SUFFIXES: .asm $(EXT)

ALL= div.spl ex2.spl ex3.spl ex4.spl ex5.spl ex6.spl ex.spl fib.spl gcd.spl hello.spl oper.spl printi.spl prio.spl tri.spl

all::
	for i in $(ALL:%.spl=%); do $(MAKE) $(MFLAGS) $$i; done

gas::
	for i in $(ALL:%.spl=%); do $(MAKE) $(MFLAGS) AS=as LD=ld $$i; done

gcc::
	for i in $(ALL:%.spl=%); do $(MAKE) $(MFLAGS) AS=as LD=gcc LIB=../librunc.a $$i; done

run::
	for i in $(ALL:%.spl=%.run); do $(MAKE) $(MFLAGS) $$i; done

$(EXT).o:
	$(EXE) $< $*.asm $(ARCH) $(DEBUG)
	$(AS) $*.asm -o $@

%: %$(EXT)
	$(EXE) $< $*.asm $(ARCH) $(DEBUG)
	$(AS) $*.asm -o $*.o
	$(LD) -o $@ $*.o $(LIB)

clean::
	rm -f *.asm *.o $(ALL:%.spl=%)

div.run: div
	echo 144 | ./div
ex2.run: ex2
	./ex2
ex3.run: ex3
	./ex3
ex4.run: ex4
	./ex4 < ex4.in
ex5.run: ex5
	echo 12 | ./ex5
ex6.run: ex6
	echo 21 | ./ex6
ex.run: ex
	./ex
fib.run: fib
	echo 12 | ./fib
gcd.run: gcd
	./gcd < ./gcd.in
oper.run: oper
	./oper < oper.in
prio.run: prio
	./prio
hello.run: hello
	./hello
printi.run: printi
	./printi
tri.run: tri
	./tri < ./tri.in
