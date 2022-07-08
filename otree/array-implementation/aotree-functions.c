#include "aotree.h"
#include <stdio.h>
#include <stdlib.h>

anode* new_anode(int maxch){
    anode* n = (struct arraynode*)malloc(sizeof(struct arraynode));

    n->maxch=maxch;
    n->parent=NULL;
    n->nch=0;
    n->children = (struct arraynode**)malloc(sizeof(struct arraynode*) * maxch);
    n->children[0]=NULL;
    return n;
}

//helper function for print_tree_as_dyck
void print_atree_rec(anode* n){
    if(n== NULL){
	return;
    }

    /* node* child = n->left_child; */

    int i = n->nch;
    while(i > 0){
	putchar('1');
	/* putchar(','); */
	print_atree_rec(n->children[i]);
	i--;
	putchar('0');
	/* putchar(','); */
    }

   return;
}

void print_atree_as_dyck(anode* n){
    print_atree_rec(n);
    putchar('\n');
    return;
}
