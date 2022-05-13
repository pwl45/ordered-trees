#include <stdio.h>
#include <stdlib.h>


typedef struct ll_node {
    int data;
    struct ll_node* next;
} ll_node;

//make ll_node
ll_node* new_llnode(int data,ll_node* next){
    ll_node* node = (ll_node*) malloc(sizeof(ll_node));
    node->data=data;
    node->next=next;
    return node;
}
//get first lukasiewicz word
ll_node* get_initial_luka(int t){
    ll_node* tl = new_llnode(0,NULL);
    ll_node* curr = tl;
    for(int i = 0; i < t-2; i++)
	curr=new_llnode(1,curr);	
    curr=new_llnode(0,curr);
    curr=new_llnode(2,curr);
    return curr;
}

void print_ll(ll_node* hd,int n){
    while(hd){
        printf("%d",hd->data);
	hd=hd->next;
    }
    putchar('\n');
}

//equivalent to pull(A,B) where B is a path beginning at p and ending at pathtl.
void pathpull(ll_node* dest, ll_node* p, ll_node* pathtl){
    ll_node* tmp = dest->next;

    dest->next=p->next;
    p->next=pathtl->next;
    pathtl->next=tmp;

    p->data--;
    dest->data++;
}

//hd is first symbol, the root of the ordered tree
//lf is the first 0; leftmost leaf of ordered tree
//lo is the first non-zero number following a 0; first branchiing in an ordered tree
//lp is p in an ordered tree (parent of first branching)
//lg is g in an ordered tree (parent of p)
void coolLuka(int t) {
    ll_node *lf, *lo, *lp, *lg;
    ll_node *hd = lp = get_initial_luka(t);
    lf=hd->next;
    lo=lf->next;

    print_ll(hd,t);
    while (lo) {
	if (lo->data) { // if o has a child, shift 1
	    pathpull(lo,lp,lf); //pull(O,P)
	    lg = lp;
	    lp = lo;
	} else {
	    if (lp == hd) { //p==root
		pathpull(lo,lp,lf); //pull(O,P)
	    } else {
		pathpull(lg,lp,lf); //pull(G,P)
		pathpull(hd,lp,lo); //pull(root,P)
		lp = hd;
		lf = hd->next;
	    }
	}
	print_ll(hd,t);
	lo = lf->next; //this is always what happens
    }
}

int main(int argc, char **argv) {
  coolLuka(atoi(argv[1]));
}
