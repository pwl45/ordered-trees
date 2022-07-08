.PHONY: all

CFLAGS=-O3

all: otree coolDyck otree-standalone lukan lukapull lukapull.s mcer otree-noparent

otree-functions.o: otree-functions.c
	gcc -c otree-functions.c $(CFLAGS)

otree: otree.c otree-functions.o 
	gcc -o otree otree.c otree-functions.o $(CFLAGS)

otree-standalone: otree-standalone.c
	gcc -o otree-standalone otree-standalone.c $(CFLAGS)

otree-noparent: otree-noparent.c
	gcc -o otree-noparent otree-noparent.c $(CFLAGS)

coolDyck: coolDyck.c
	gcc -o coolDyck coolDyck.c $(CFLAGS)

lukan: lukan.c
	gcc -o lukan lukan.c $(CFLAGS)

lukapull: lukapull.c
	gcc -o lukapull lukapull.c $(CFLAGS)

lukapull.s: lukapull.c
	gcc -S -fverbose-asm lukapull.c $(CFLAGS)

mcer: mcer.c
	gcc -o mcer mcer.c $(CFLAGS)

.PHONY: clean
clean:
	rm -f otree-functions.o otree otree-standalone aotree-functions.o oluka.o aotree coolDyck lukan lukapull lukapull.s mcer
