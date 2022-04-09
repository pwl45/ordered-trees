#include "otree.h"
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

node* new_node(int data){
    node* n = (struct node*)malloc(sizeof(struct node));

    n->data=data;
    /* n->nchildren=0; */
    n->parent=NULL;
    n->left_child=NULL;
    n->right_sibling=NULL;
    return n;

}

void printdyck(uint8_t* b, int n){

    /* return; */

    for(int i = 0; i < n-1; i++){
	putchar(b[i+1]+48);
	/* putchar(','); */
	/* printf("%c,",(b[i+1]+48)); */
    }
    putchar(b[n+1]+48);
    putchar('\n');
    /* printf("\n"); */
}

//not currently used: convert a tree to a buffer of 0/1 uint8_ts 
//call as tree_to_dyck_arr(root,b,1) to preserve 1-based indexing.
int tree_to_dyck_arr(node* n, uint8_t* buf, int off){
    if(n== NULL){
	return 0;
    }

    node* child = n->left_child;

    //if node has no children, this while loop is skipped and off is preserved
    while(child != NULL){
	//record a 1 for the current child
	buf[off] = 1;

	//pass offset+1 to recursive call, traverse child's subtree
	off = tree_to_dyck_arr(child,buf,off+1);

	//write a zero reflecting the move back up to the parent and increment offset
	buf[off] = 0;
	off += 1;

	//move to next child if it exists
	child = child->right_sibling;
    }

    return off;
}

//helper function for print_tree_as_dyck
void print_tree_rec(node* n){
    if(n== NULL){
	return;
    }

    node* child = n->left_child;

    while(child != NULL){
	putchar('1');
	/* putchar(','); */
	print_tree_rec(child);
	child = child->right_sibling;
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

//some stuff for latex
void qtree(node* n){

    /* printf("[.%d ",n->nchildren); */
    printf("[.%d ",0);

    node* child=n->left_child;
    while(child != NULL){
	qtree(child);
	child = child->right_sibling;
    }
    printf("] ");
}

void print_tree_as_tikz(node* n){
    printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{edge from parent/.style={draw, edge from parent path=\n{(\\tikzparentnode) -- (\\tikzchildnode)}}}\n\\Tree");
    qtree(n);
    printf("\n\\end{tikzpicture}\n\n");
}

//some stuff for latex
void binary_qtree(node* n){

    /* printf("[.%d ",n->nchildren); */
    if(!n){
	return;
    }
    printf("[.{} ");

    if(n->left_child){
	binary_qtree(n->left_child);
    }else{
	printf("\\edge[draw=none]; \\node[blank]{};");
    }

    if(n->right_sibling){
	binary_qtree(n->right_sibling);
    }else{
	printf("\\edge[draw=none]; \\node[blank]{};");
    }

    printf("] ");
}

void print_binary_tree_as_tikz(node* n){
    printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{every tree node/.style={minimum width=1.5em,draw,circle}, blank/.style={draw=none}, edge from parent/.style= {draw,edge from parent path={(\\tikzparentnode) -- (\\tikzchildnode)}}, level distance=1.5cm}\n\\Tree");
    binary_qtree(n->left_child);
    printf("\n\\end{tikzpicture}\n\n");
}
