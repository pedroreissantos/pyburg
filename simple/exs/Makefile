EXT=.spl
EXE=../simple
LIB=../libsimple.a
AS=nasm -felf32
LD=ld -m elf_i386

.SUFFIXES: .asm $(EXT)

ALL= div.spl ex2.spl ex3.spl ex4.spl ex5.spl ex6.spl ex.spl fib.spl gcd.spl prio.spl tri.spl x.spl

all::
	for i in $(ALL:%.spl=%); do $(MAKE) $(MFLAGS) $$i; done

run::
	for i in $(ALL:%.spl=%.run); do $(MAKE) $(MFLAGS) $$i; done

$(EXT).o:
	$(EXE) $< $*.asm
	$(AS) $*.asm -o $@

%: %$(EXT)
	$(EXE) $< $*.asm
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
prio.run: prio
	./prio
hello.run: hello
	./hello
printi.run: printi
	./printi
tri.run: tri
	./tri < ./tri.in
x.run: x
	./x
