#include <stdio.h>
#include <stdlib.h>
struct node {
    // i love void stars
    int data;
    int nchildren;
    struct node* parent;
    struct node* left_child;
    struct node* right_child;
    struct node* right_sibling;

    /* struct node* left_sibling; */

};

typedef struct node node;

node* new_node(int data){
    node* n = (struct node*)malloc(sizeof(struct node));

    n->data=data;
    n->nchildren=0;
    n->parent=NULL;
    n->left_child=NULL;
    n->right_child=NULL;
    n->right_sibling=NULL;
    return n;

}

//no longer used: function for getting o from a tree manually
//can be used (and used to be used) to verify correctness in certain cases 
node* get_o(node* root){
    node* o=NULL;
    node* curr=root;

    while(curr->left_child != NULL){
	if(curr->left_child->right_sibling != NULL){
	    o = curr->left_child->right_sibling;
	}
	curr = curr->left_child;
    }
    return o;
}

//some stuff for latex
void qtree(node* n){

    printf("[.%d ",n->nchildren);

    node* child=n->left_child;
    while(child != NULL){
	qtree(child);
	child = child->right_sibling;
    }
    printf("] ");
}

void latex_qtree(node* n){
    printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{edge from parent/.style={draw, edge from parent path=\n{(\\tikzparentnode) -- (\\tikzchildnode)}}}\n\\Tree");
    qtree(n);
    printf("\n\\end{tikzpicture}\n\n");
}
