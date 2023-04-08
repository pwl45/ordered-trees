.PHONY: all clean

CFLAGS=-O3

all: otree coolDyck otree-standalone otree-noparent mcer bintree bintree-rusk flextree otree-inlined

otree-functions.o: otree-functions.c
	gcc -c otree-functions.c $(CFLAGS)

otree: otree.c otree-functions.o 
	gcc -o otree otree.c otree-functions.o $(CFLAGS)

bintree: bintree.c
	gcc -o bintree bintree.c $(CFLAGS)

bintree-rusk: bintree-rusk.c
	gcc -o bintree-rusk bintree-rusk.c $(CFLAGS)

otree-standalone: otree-standalone.c
	gcc -o otree-standalone otree-standalone.c $(CFLAGS)

otree-noparent: otree-noparent.c
	gcc -o otree-noparent otree-noparent.c $(CFLAGS)

otree-inlined: otree-inlined.c
	gcc -o otree-inlined otree-inlined.c $(CFLAGS)

coolDyck: coolDyck.c
	gcc -o coolDyck coolDyck.c $(CFLAGS)

mcer: mcer.c
	gcc -o mcer mcer.c $(CFLAGS)

flextree: flextree.c
	gcc -o flextree flextree.c $(CFLAGS)

clean:
	rm -f otree-functions.o otree otree-standalone coolDyck mcer otree-noparent flextree bintree-rusk otree-inlined
