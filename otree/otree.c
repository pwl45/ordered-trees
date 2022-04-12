#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "otree.h" 

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

void coolOtree(int t, void (*visit)(node* nod), void (*push)(node* parent, node* child), node* (*pop)(node* child) ){
    node* root = get_initial_tree(t); //defined in otree-functions.c
    node* o=root->left_child->right_sibling;

    visit(root);

    while(o){
	if(o->left_child){ //if o has a child, shift 1
	    push(o,pop(o->parent));
	    o=o->left_child->right_sibling;
	}else{
	    if(o->parent == root){ //if the string is tight, shift a 1
		push(o,pop(o->parent));
	    }else{ //if the string isn't tight, shift a zero
		node* p = o->parent;
		push(p->parent,pop(p));
		push(root,pop(p));
	    }
	    o=o->right_sibling;
	}
	visit(root);
    }
}

int main(int argc, char** argv){
    //not exactly bulletproof
    /* coolOtree(atoi(argv[1]), print_tree_as_dyck); */

    int t = 0;

    //void function that takes a node* as a parameter, 
    //intended to visit the tree with the parameter node as its root
    void (*visit)(node*)=print_tree_as_dyck;


    //void function that takes an int and a visiting function (like the one above) as paremeters
    void (*generate)(int t, void (*visit)(node*), void (*push)(node*, node*), node* (*pop)(node*))=coolOtree;
    void (*push)(node*, node*)=pushchild;
    node* (*pop)(node*)=popchild;

    //parse arguments
    for(int i = 1; i < argc; i++){
	if(argv[i][0] == '-'){
	    int len = strlen(argv[i]);
	    for(int j = 1; j < len; j++){
		char argchar = argv[i][j];
		if(argchar == 'b'){ //bintree: print as tikz for binary tree
		    visit = print_bintree_as_tikz;
		}else if(argchar == 'o'){ //otree: print as tikz for ordered trees
		    visit = print_otree_as_tikz;
		}else if(argchar == 'f'){ //flexible: maintain parent pointer for binary tree (right_sibling)
		    push=pushchild_flex;
		    pop=popchild_flex;
		}else{
		    fprintf(stderr, "Invalid argument -%c\n",argchar);
		    exit(1);
		}
	    }
	}else{
	    //not exactly bulletproof
	    t = atoi(argv[i]); 
	}
    }

    if(t <= 0){
	fprintf(stderr, "Missing/Invalid value for n: %d\nUsage: ./otree [args] n\n",t);
	exit(1);
    }

    generate(t, visit,push,pop);
}
