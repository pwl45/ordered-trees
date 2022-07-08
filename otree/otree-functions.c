#include "otree.h"
#include <stdio.h>
#include <stdlib.h>

node* new_node(int data){
    node* n = (node*)malloc(sizeof(node));

    n->data=data;
    /* n->nchildren=0; */
    n->parent=NULL;
    n->first=NULL;
    n->right=NULL;
    return n;

}

void printdyck(uint8_t* b, int n){
    for(int i = 0; i < n-1; i++){
	putchar(b[i+1]+48);
    }
    putchar(b[n+1]+48);
    putchar('\n');
}

//not currently used: convert a tree to a buffer of 0/1 uint8_ts 
//call as tree_to_dyck_arr(root,b,1) to preserve 1-based indexing.
int tree_to_dyck_arr(node* n, uint8_t* buf, int off){
    if(n== NULL){
	return 0;
    }

    node* child = n->first;

    while(child != NULL){
	//record a 1 for the current child
	buf[off] = 1;

	//pass offset+1 to recursive call, traverse child's subtree
	off = tree_to_dyck_arr(child,buf,off+1);

	//write a zero reflecting the move back up to the parent and increment offset
	buf[off] = 0;
	off += 1;

	//move to next child if it exists
	child = child->right;
    }

    return off;
}

//helper function for print_tree_as_dyck
void print_tree_rec(node* n){
    if(n== NULL){
	return;
    }
    node* child = n->first;
    while(child != NULL){
	putchar('1');
	/* putchar(','); */
	print_tree_rec(child);
	child = child->right;
	putchar('0');
	/* putchar(','); */
    }
   return;
}


//prints an ordered tree as a dyck word
void print_tree_as_dyck(node* n){
    print_tree_rec(n);
    putchar('\n');
    return;
}

//get the tree corresponding to 101^{t-1}0^{t-1}
node* get_initial_tree(int t){
    node* root = new_node(0);
    root->first=new_node(1);
    root->first->parent=root;

    if(t > 1){
	node* curr = new_node(2);
	curr->parent=root;
	root->first->right=curr;
	for(int i = 2; i < t; i++){
	    node* next = new_node(i+1);
	    curr->first=next;
	    next->parent=curr;
	    curr=next;
	}
    }
    return root;
}

//some stuff for latex
void qtree(node* n){
    printf("[.{} ");

    node* child=n->first;
    while(child != NULL){
	qtree(child);
	child = child->right;
    }
    printf("] ");
}



void print_otree_as_tikz(node* n){
    printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{every tree node/.style={minimum width=1.5em,draw,circle}, blank/.style={draw=none}, edge from parent/.style= {draw,edge from parent path={(\\tikzparentnode) -- (\\tikzchildnode)}}, level distance=1.5cm}\n\\Tree");
    qtree(n);
    printf("\n\\end{tikzpicture}\\hspace{1.5em}\n");
}

void lukatree_rec(node* n){
    if(!n){
	return;
    }

    node* curr = n->first;
    int i = 0;
    while(curr){
	i++;
	curr=curr->right;
    }
    printf("%d",i);
    curr = n->first;
    while(curr){
	lukatree_rec(curr);
	curr=curr->right;
    }
}

// Print an ordered tree as a Lukasiewicz word
void print_otree_as_luka(node* n){
    lukatree_rec(n);
    printf("\n");
}
