COMP=python3 ../code.py
EXT=.b
LDLIBS=../../run/librun.a
.SUFFIXES: $(EXT) .asm
#AS=nasm -felf32
AS=as -o $@
#LD=ld -melf_i386 # 32-bit binaries in a 64-bit system
LD=ld

SRC= 1.b 2.b 3.b 4.b ack.b blanks.b bubble.b convert.b div.b \
	duzia.b empty.b fib.b fibiter.b flip.b gcd.b getput.b getstring.b \
	hello.b hi.b histograma.b incr.b iter.b lower.b main.b mfind.b \
	mins.b minar.b nep.b novrfl.b powfunc.b printf.b \
	printn.b prog.b r.b recurs.b snide.b strcp.b \
	tab.b testfit.b tri.b world.b z.b

EXE=$(SRC:%.b=%)

all:: $(EXE)

arm::
	$(MAKE) $(MFLAGS) AS="as"

i386::
	$(MAKE) $(MFLAGS) LD="ld --melf_i386" AS="nasm -felf32"

linux32::
	$(MAKE) $(MFLAGS) AS="nasm -felf32"

linux64::
	$(MAKE) $(MFLAGS) AS="nasm -felf64"

x64::
	$(MAKE) $(MFLAGS) AS="as" LD="ld"

test:: all
	(cd test; ./run)

iter: iter.o fact.o
	$(LD) -o $@ $^ $(LDLIBS)
recurs: recurs.o fact.o
	$(LD) -o $@ $^ $(LDLIBS)
flip: flip.o printn.o
	$(LD) -o $@ $^ $(LDLIBS)
getstring: getstring.o getstrng.o
	$(LD) -o $@ $^ $(LDLIBS)
testfit: testfit.o fit.o
	$(LD) -o $@ $^ $(LDLIBS)
empty: empty.o hello.o
	$(LD) -o $@ $^ $(LDLIBS)
powfunc: powfunc.o power.o
	$(LD) -o $@ $^ $(LDLIBS)
mfind: find.o mfind.o
	$(LD) -o $@ $^ $(LDLIBS)
mins: mins.o min.o
	$(LD) -o $@ $^ $(LDLIBS)
minar: mins.o minar.o
	$(LD) -o $@ $^ $(LDLIBS)
lower: lower.o tolower.o char.o
	$(LD) -o $@ $^ $(LDLIBS)
printf: printf.o printn.o printfunc.o
	$(LD) -o $@ $^ $(LDLIBS)
world: printf.o printn.o world.o
	$(LD) -o $@ $^ $(LDLIBS)
printn: printn.o printnum.o
	$(LD) -o $@ $^ $(LDLIBS)
convert: convert.o conv.o char.o printn.o printf.o
	$(LD) -o $@ $^ $(LDLIBS)
snide: snide.o unit.o char.o printn.o printf.o
	$(LD) -o $@ $^ $(LDLIBS)
strcp: strcp.o strcopy.o char.o
	$(LD) -o $@ $^ $(LDLIBS)
bubble: bubble.o sort.o fit.o string.o
	$(LD) -o $@ $^ $(LDLIBS)
cmp: cmp.o string.o fit.o
	$(LD) -o $@ $^ $(LDLIBS)
z: z.o char.o
	$(LD) -o $@ $^ $(LDLIBS)

%: %.o
	$(LD) -o $@ $< $(LDLIBS)

.asm.o:
	$(AS) $< -o $@

.b.asm:
	$(COMP) $< $@

clean:
	rm -rf a.out *~ *.o *.asm $(EXE) ../parser.out ../parsetab.py ../__pycache__
