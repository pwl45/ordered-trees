#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "otree.h" 

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

int print_tree_rec(node* n){
    if(n== NULL){
	return 0;
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

    return 0;

}

void print_tree_as_dyck(node* n){
    print_tree_rec(n);
    putchar('\n');
    return;
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



//mnemonics: 
//l is left of o
//p is o's parent
//pp is o's parent's parent
void shift_tree_zero(node* root, node* o){
    /* if(o == NULL) */
	// to make this work for the non-increasing (111...000...) case, do something here
	// right now, the loop ends on the non-increasing string, so this case isn't necessary

    //get l,p,pp
    node* p = o->parent;
    node* l = p->left_child;
    node* pp = p->parent;

    //setup p
    //new left_child is l's right sibling
    /* printf(" setup p\n"); */
    p->left_child=o->right_sibling;

    //setup l
    //new right sibling is old parent
    //new parent is parent's parent
    l->parent=pp;
    l->right_sibling=p;
    pp->left_child=l;

    //note: O shift must come after l shift
    //push o up to root;
    o->parent=root;
    o->right_sibling=root->left_child;
    root->left_child=o;
}

void shift_tree_one(node* root, node* o){
    //get l
    node* l = o->parent->left_child;

    //make l o's first child
    o->parent->left_child=o;
    l->parent=o;
    l->right_sibling=o->left_child;
    o->left_child=l;
}

//get the tree corresponding to 101^{t-1}0^{t-1}
node* get_initial_tree(int t){
    node* root = new_node(0);
    root->left_child=new_node(1);
    root->left_child->parent=root;
    
    node* o = NULL;
    if(t > 1){
	o = new_node(2);
	o->parent=root;
	root->left_child->right_sibling=o;
	node* curr=o;
	for(int i = 2; i < t; i++){
	    node* next = new_node(i+1);
	    curr->left_child=next;
	    next->parent=curr;
	    /* curr->left_child = */ 
	    curr=next;
	}
    }
    return root;

}

void coolOtree(int t, void (*visit)(node*)){
    int n = 2*t;

    node* root = get_initial_tree(t);
    node* o=root->left_child->right_sibling;

    uint8_t* b = (uint8_t*) malloc(sizeof(uint8_t)*(n+1));
    visit(root);

    while(o){
	if(o->left_child){ //if o has a child, shift 1
	    shift_tree_one(root,o);
	    o=o->left_child->right_sibling;
	}else{
	    if(o->parent == root){ //if the string is tight, shift a 1
		shift_tree_one(root,o);
		o=o->right_sibling;
	    }else{ //if the string isn't tight, shift a zero
		shift_tree_zero(root,o);
		o=o->right_sibling;
	    }
	}
	visit(root);
    }
}

int main(int argc, char** argv){
    //not exactly bulletproof
    if(argc < 2)
	exit(1);

    //todo: parse command line arguments to change the visit function
    coolOtree(atoi(argv[1]), print_tree_as_dyck);
    /* coolOtree(atoi(argv[1]), latex_qtree); */

}
