//clot: (c)ool-(l)ex (o)rdered (t)rees
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

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

int print_tree_as_dyck(node* n){
    print_tree_rec(n);
    putchar('\n');
    return 0;
}

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
    printf("\n\\end{tikzpicture}");
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

//mnemonics: 
//l is left of o
//p is o's parent
//pp is o's parent's parent
void shift_tree_zero(node* root, node* o){
    /* if(o == NULL) */
	// to make this work for the non-increasing (111...000...) case, do something here
	// right now, the loop ends on the non-increasing string, so this case isn't necessary

    //get l,p,pp
    node* l = o->parent->left_child;
    node* p = l->parent;
    node* pp = l->parent->parent;

    //setup p
    //new left_child is l's right sibling
    /* printf(" setup p\n"); */
    p->left_child=o->right_sibling;

    //setup l
    //new right sibling is old parent
    //new parent is parent's parent
    l->parent=pp;
    l->right_sibling=pp->left_child;
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

void coolOtree(int t){
    int n = 2*t;

    node* root = get_initial_tree(t);
    node* o=root->left_child->right_sibling;

    uint8_t* b = (uint8_t*) malloc(sizeof(uint8_t)*(n+1));
    print_tree_as_dyck(root);

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
	print_tree_as_dyck(root);
    }
}

int main(int argc, char** argv){
    if(argc < 2)
	exit(1);
    coolOtree(atoi(argv[1]));
}
