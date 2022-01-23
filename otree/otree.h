#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
struct node {
    // i love void stars
    int data;
    int nchildren;
    struct node* parent;
    struct node* left_child;
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
int tree_to_dyck_arr(node* n, uint8_t* buf, int off){
    if(n== NULL){
	return 0;
    }


    node* child = n->left_child;

    int ret = 0;
    while(child != NULL){
	buf[off] = 1;
	off = tree_to_dyck_arr(child,buf,off+1);
	child = child->right_sibling;
	buf[off] = 0;
	off += 1;
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

    printf("[.%d ",n->nchildren);

    node* child=n->left_child;
    while(child != NULL){
	qtree(child);
	child = child->right_sibling;
    }
    printf("] ");
}

void print_tree_as_latex(node* n){
    printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{edge from parent/.style={draw, edge from parent path=\n{(\\tikzparentnode) -- (\\tikzchildnode)}}}\n\\Tree");
    qtree(n);
    printf("\n\\end{tikzpicture}\n\n");
}
