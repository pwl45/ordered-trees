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

//get the tree corresponding to 101^{t-1}0^{t-1}; maintain right_sibling pointer
node* get_initial_tree_flex(int t){
    node* root = new_node(0);
    //TODO: factor out root->left_child
    root->left_child=new_node(1);
    root->left_child->parent=root;
    
    node* o = NULL;
    if(t > 1){
	o = new_node(2);
	o->parent=root;
	root->left_child->right_sibling=o;
	o->left_sibling=root->left_child;
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

//versions that do not maintain the left_sibling pointer (binary tree parent)
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

//versions that maintain the left_sibling pointer (binary tree parent)
node* popchild_flex(node* nod){
    node* result = nod->left_child;
    node* rsib = result->right_sibling;
    nod->left_child= rsib;
    if(rsib){
	rsib->left_sibling = NULL;
    }
    return result;
}
void pushchild_flex(node* parent, node* child){
    node* rsib = parent->left_child;
    child->right_sibling=rsib;
    if(rsib){
	rsib->left_sibling = child;
    }
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

void coolOtree_flex(int t, void (*visit)(node*)){
    node* root = get_initial_tree_flex(t);
    node* o=root->left_child->right_sibling;

    visit(root);

    while(o){
	node* p = o->parent;
	if(o->left_child){ //if o has a child, shift 1
	    /* printf("1\n"); */
	    pushchild_flex(o,popchild_flex(p));
	    o=o->left_child->right_sibling;
	}else{
	    if(o->parent == root){ //if the string is tight, shift a 1
		/* printf("%p\n",o); */
		/* printf("2\n"); */
		node* idk = popchild_flex(p);
		/* printf("past popchild\n"); */
		/* printf("%p %p\n",o,idk); */
		pushchild_flex(o,idk);
	    }else{ //if the string isn't tight, shift a zero
		/* printf("3\n"); */
		pushchild_flex(p->parent,popchild_flex(p));
		pushchild_flex(root,popchild_flex(p));
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
    /* coolOtree(atoi(argv[1]), print_tree_as_dyck); */
    coolOtree_flex(atoi(argv[1]), print_binary_tree_as_tikz);
    /* coolOtree(atoi(argv[1]), print_tree_as_tikz); */
}
