.PHONY: all

CFLAGS=-O0

all: otree coolDyck otree-simple

otree-functions.o: otree-functions.c
	gcc -c otree-functions.c $(CFLAGS)

otree: otree.c otree-functions.o
	gcc -o otree otree.c otree-functions.o $(CFLAGS)

otree-simple: otree-simple.c otree-functions.o
	gcc -o otree-simple otree-simple.c otree-functions.o $(CFLAGS)

coolDyck: coolDyck.c
	gcc -o coolDyck coolDyck.c $(CFLAGS)

.PHONY: clean
clean:
	rm -f otree otree-old otree-functions.o coolDyck
