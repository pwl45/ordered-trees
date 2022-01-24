.PHONY: all
all: otree coolDyck

otree-functions.o: otree-functions.c
	gcc -c otree-functions.c

otree: otree.c otree-functions.o
	gcc -o otree otree.c otree-functions.o

coolDyck: coolDyck.c
	gcc -o coolDyck coolDyck.c

.PHONY: clean
clean:
	rm -f otree otree-functions.o coolDyck
