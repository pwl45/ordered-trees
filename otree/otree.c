#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "otree.h" 
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

node* popchild(node* nod){
    node* result = nod->left_child;
    nod->left_child=result->right_sibling;
    return result;
}

void pushchild(node* parent, node* child){
    child->right_sibling=parent->left_child;
    parent->left_child=child;
    child->parent=parent;
}

void coolOtree(int t, void (*visit)(node*)){
    node* root = get_initial_tree(t);
    node* o=root->left_child->right_sibling;

    visit(root);

    while(o){
	if(o->left_child){ //if o has a child, shift 1
	    pushchild(o,popchild(o->parent));
	    o=o->left_child->right_sibling;
	}else{
	    if(o->parent == root){ //if the string is tight, shift a 1
		pushchild(o,popchild(o->parent));
	    }else{ //if the string isn't tight, shift a zero
		node* p = o->parent;
		pushchild(p->parent,popchild(p));
		pushchild(root,popchild(p));
	    }
	    o=o->right_sibling;
	}
	visit(root);
    }
}

int main(int argc, char** argv){
    //not exactly bulletproof
    if(argc < 2)
	exit(1);
    coolOtree(atoi(argv[1]), print_tree_as_dyck);
    /* coolOtree(atoi(argv[1]), print_tree_as_tikz); */
}
