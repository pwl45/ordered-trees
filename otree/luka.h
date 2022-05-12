#include <stdio.h>
#include <stdlib.h>
#include "otree.h"

//linked list node struct
typedef struct ll_node {
    char data;
    struct ll_node* prev;
    struct ll_node* next;
} ll_node;

ll_node* getluka(node* n);
void print_ll(ll_node* hd);
ll_node* new_llnode(int data, ll_node* prev, ll_node* next);
