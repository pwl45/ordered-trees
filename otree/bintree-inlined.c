#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
typedef struct node { struct node *left; struct node *right; } node;
typedef struct bintreenode { struct bintreenode* left; struct bintreenode* right;} bintreenode;

// Has trailing zero for now
void visit_bintree_rec(node* n){
  if (n == NULL){
    putchar('0');
    return;
  }else{
    putchar('1');
  }
  visit_bintree_rec(n->left);
  visit_bintree_rec(n->right);
}

// otree root->left is start of binary tree
void visit(node* root){ visit_bintree_rec(root->left); putchar('\n');}

void coolBintree(int n) {
  node *root = (node*)calloc(sizeof(node),1);
  node *prev, *curr = root;
  for(int i = 0; i < n; i++){
    curr->left = (node*)calloc(sizeof(node),1);
    prev=curr;
    curr=curr->left;
  }
  pull(root,prev);
  node *p=root, *g=NULL, *o = root->left->right, *pulled=NULL;
  visit(root);
  while (o) {
    if (o->left) { // if o has a child, o pulls p
      g=p;
      pulled = p->left;
      p = p->left = o;
      pulled->right = o->left;
      o->left = pulled;
      o = pulled->right;
    } else {
      if (p == root) { // if p is the root, o pulls p
        pulled = p->left;
        p->left = o;
        pulled->right = o->left;
        o->left = pulled;
      } else { // otherwise, g pulls p and root pulls p
        p->left->right = p;
        g->left = p->left;
        p->left = o->right;
        o->right = root->left;
        root->left = o;
        p=root; //g could be set to null
      }
      o = o->right;
    }
    visit(root);
  }
}
int main(int argc, char **argv) { coolBintree(atoi(argv[1])); }
