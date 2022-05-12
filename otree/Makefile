.PHONY: all

CFLAGS=-O3

all: otree coolDyck aotree otree-standalone lukan

otree-functions.o: otree-functions.c
	gcc -c otree-functions.c $(CFLAGS)

otree: otree.c otree-functions.o oluka.o
	gcc -o otree otree.c oluka.o otree-functions.o $(CFLAGS)

otree-standalone: otree-standalone.c
	gcc -o otree-standalone otree-standalone.c $(CFLAGS)

aotree-functions.o: aotree-functions.c
	gcc -c aotree-functions.c $(CFLAGS)

oluka.o: oluka.c
	gcc -c oluka.c $(CFLAGS)

aotree: aotree.c aotree-functions.o otree-functions.o
	gcc -o aotree aotree.c otree-functions.o aotree-functions.o $(CFLAGS)

coolDyck: coolDyck.c
	gcc -o coolDyck coolDyck.c $(CFLAGS)

lukan: lukan.c
	gcc -o lukan lukan.c $(CFLAGS)


.PHONY: clean
clean:
	rm -f otree otree-old otree-functions.o coolDyck aotree aotree-functions.o oluka.o lukan 
