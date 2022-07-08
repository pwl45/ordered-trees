#include <inttypes.h>

typedef struct node {
    int data; //not  strictly necessary
    struct node* parent;
    struct node* first; //binary tree left
    struct node* right; //binary tree right

} node;

/* typedef struct node node; */

//function for allocating and initializing a node
node* new_node(int data);

//convert a tree to a dyck word and store the result in buf
//buf is an already malloced buffer of size equal to the length of the resulting dyck word
int tree_to_dyck_arr(node* n, uint8_t* buf, int off);

//printing functions
void printdyck(uint8_t* b, int n); //print dyck word as ones and zeroes
void print_tree_as_dyck(node* n); //print tree as dyck word
void print_otree_as_luka(node* n);
void qtree(node* n); //print just \Tree calls to generate qtrees
void print_otree_as_tikz(node* n); //print whole tikzpicture
/* void print_bintree_as_tikz(node* n); */
void print_tree_as_tikz(node* n);

node* get_initial_tree(int t);
