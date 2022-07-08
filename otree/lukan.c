#include <stdio.h>
#include <stdlib.h>


typedef struct ll_node {
    char data;
    struct ll_node* next;
} ll_node;

ll_node* new_llnode(int data, ll_node* prev, ll_node* next){
    ll_node* node = (ll_node*) malloc(sizeof(ll_node*));
    node->data=data;
    node->next=next;
    return node;
}
ll_node* get_initial_luka(int t){
    ll_node* hd = new_llnode(2,NULL,NULL);
    ll_node* curr = new_llnode(0,NULL,NULL);
    hd->next=curr;
    
    for(int i = 0; i < t-2; i++){
	curr->next=new_llnode(1,NULL,NULL);	
	curr=curr->next;
    }

    //we need the final leaf 0
    curr->next=new_llnode(0,NULL,NULL);

    return hd;
}

void print_ll(ll_node* hd,int n){
    return;
    if(hd){
        printf("%d",hd->data);
    }
    while( (hd=hd->next) ){
        printf("%d",hd->data);
    }
    printf("\n");
}


//hd is first symbol, the root of the ordered tree
//lf is the first 0; leftmost leaf of ordered tree
//lo is the first non-zero number following a 0; first branchiing in an ordered tree
//lp is p in an ordered tree (parent of first branching)
//lg is g in an ordered tree (parent of p)
void coolLuka(int t) {
    ll_node *lf, *lo, *lp, *lg;
    ll_node *hd = get_initial_luka(t);
    lf=hd->next;
    lo=lf->next;
    lp=hd;
    lg=NULL;

    print_ll(hd,t);
    while (lo) {
	if (lo->data) { // if o has a child, shift 1

	    //pull(O,P)
	    lf->next = lo->next;
	    lo->next = lp->next;
	    lp->next = lo;
	    lp->data--;
	    lo->data++;

	    lg = lp;
	    lp = lo;
	} else {
	    if (lp == hd) { // if the string is tight, shift a 1

		//pull(O,P)
		lf->next = lo->next;
		lo->next = lp->next;
		lp->next = lo;
		lp->data--;
		lo->data++;

		//don't even need to update anything here, nice
		/* lg = NULL; */ 
		/* lp = lp; */
		/* lf = lf */
	    } else { // if the string isn't tight, shift a zero

		//pull(G,P)
		lg->data++;
		lp->data--;
		lf->next = lp; // lf->next=lo;
		lg->next = lp->next;
		/* lp->next = lo; // this will be overwritten by the next block anyway*/
		hd->data++;

		//pull(root,P)
		lp->data--;
		lp->next = lo->next; // works because o has no children
		lo->next = hd->next;
		hd->next = lo;

		/* lg = NULL; //there is no lg, but it won't be accessed so don't need to NULL it */
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
