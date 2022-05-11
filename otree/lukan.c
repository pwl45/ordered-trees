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

void print_ll(ll_node* hd){
    if(hd){
        printf("%d",hd->data);
    }
    while( (hd=hd->next) ){
        printf("%d",hd->data);
    }
    printf("\n");
}


void coolLuka(int t) {
    ll_node *lf, *lo, *lp, *lg;
    ll_node *hd = get_initial_luka(t);
    lf=hd->next;
    lo=lf->next;
    lp=hd;
    lg=NULL;

    print_ll(hd);
    while (lo) {
	if (lo->data) { // if o has a child, shift 1

	    lf->next = lo->next;
	    lo->next = lp->next;
	    lp->next = lo;
	    lp->data--;
	    lo->data++;

	    lg = lp;
	    lp = lo;
	    lo = lf->next;
	} else {
	    if (lp == hd) { // if the string is tight, shift a 1

		lf->next = lo->next;
		lo->next = lp->next;
		lp->next = lo;
		lp->data--;
		lo->data++;

		lg = NULL;
		lp = lp;
		lo = lf->next;
	    } else { // if the string isn't tight, shift a zero

		lg->data++;
		lp->data--;
		lf->next = lp; // lf->next=o;
		lg->next = lp->next;
		lp->next = lo;
		hd->data++;

		lp->data--;
		lp->next = lo->next; // works because o has no children
		lo->next = hd->next;
		hd->next = lo;

		lg = NULL;
		lp = hd;
		lf = hd->next;
		lo = lf->next;
	    }
	}
	print_ll(hd);

    }
}

int main(int argc, char **argv) {
  coolLuka(atoi(argv[1]));
}
