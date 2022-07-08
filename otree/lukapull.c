#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


typedef struct lukanode {
    int value;
    struct lukanode* next;
} lukanode;

//make lukanode
lukanode* new_llnode(int value,lukanode* next){
    lukanode* node = (lukanode*) malloc(sizeof(lukanode));
    node->value=value;
    node->next=next;
    return node;
}
//get first lukasiewicz word
lukanode* get_initial_luka(int t){
    /* printf("initluka\n"); */
    lukanode* tl = new_llnode(0,NULL);
    lukanode* curr = tl;
    for(int i = 0; i < t-2; i++)
	curr=new_llnode(1,curr);	
    curr=new_llnode(0,curr);
    curr=new_llnode(2,curr);
    /* printf("done initluika\n"); */
    return curr;
}

void print_ll(lukanode* hd,int n){
    while(hd){
        printf("%d",hd->value);
	hd=hd->next;
    }
    putchar('\n');
}

//bad
void swap3(uintptr_t* A, uintptr_t* B, uintptr_t* C){
    *A = (*A) ^ (*B) ^ (*C);
    *B = (*A) ^ (*B) ^ (*C);
    *C = (*A) ^ (*B) ^ (*C);
    *A = (*A) ^ (*B) ^ (*C);
}

//equivalent to pull(A,B) where B is a path beginning at p and ending at pathtl.
void pathpull(lukanode* dest, lukanode* p, lukanode* pathtl){

    lukanode* tmp = dest->next;
    dest->next=p->next;
    p->next=pathtl->next;
    pathtl->next=tmp;

    p->value--;
    dest->value++;
}

void lshift(lukanode* src, lukanode* dest){
    lukanode* shifted = src->next;
    src->next=shifted->next;
    shifted->next=dest->next;
    dest->next=shifted;
}


//hd is first symbol, the root of the ordered tree
//lf is the first 0; leftmost leaf of ordered tree
//lo is the first non-zero number following a 0; first branchiing in an ordered tree
//lp is p in an ordered tree (parent of first branching)
//lg is g in an ordered tree (parent of p)
void coolLuka(int t) {
    lukanode *lf, *lo, *lp, *lg;
    lukanode *hd = lp = get_initial_luka(t);
    lf=hd->next;
    lo=lf->next;

    /* int i=0; */
    print_ll(hd,t);
    while (lo) {
	if (lo->value) { // if o has a child, shift 1
	    /* pathpull(lo,lp,lf); //pull(O,P) */
	    lshift(lf,lp);
	    lp->value--;
	    lo->value++;
	    lg = lp;
	    lp = lo;
	} else {
	    if (lp == hd) { //p==root
		lshift(lf,lp);
		lp->value--;
		lo->value++;
	    } else {
		lshift(lg,lf);
		lp->value--;
		lg->value++;
		lshift(lp,hd);
		lp->value--;
		hd->value++;

		lp = hd;
		lf = hd->next;
	    }
	}
	print_ll(hd,t);
	lo = lf->next; //this is always what happens
	/* i++; */
    }
}

int main(int argc, char **argv) {
  /* coolLuka(atoi(argv[1])); */
  coolLuka(atoi(argv[1]));
}
