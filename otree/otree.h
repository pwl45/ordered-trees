#include <inttypes.h>
#define N_MARKED 4
#define MARK_O -1
#define MARK_P -2
#define MARK_L -3
#define MARK_G -4

typedef struct node {
    int data; //not  strictly necessary
    struct node* parent;
    struct node* left_child; //binary tree left
    struct node* right_sibling; //binary tree right

    //not necessary for ordered tree
    struct node* left_sibling; //binary tree parent
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
void print_bintree_as_tikz(node* n);
void print_tree_as_tikz(node* n);
void fancy_otree_tikz(node* n);
void illustrate_shifts(node* root);
void iterate_once(node* root, node* o);


node* get_initial_tree(int t);
node* get_initial_tree_flex(int t);
