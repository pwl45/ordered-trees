#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
typedef struct node { struct node *left; struct node *right; } node;
typedef struct bintreenode { struct bintreenode* left; struct bintreenode* right;} bintreenode;

void pull(node *A, node *B){ 
  node *pulled = B->left;
  B->left = pulled->right;
  pulled->right = A->left;
  A->left = pulled;
}

//P is the parent of the rotation point (we don't store parent pointer, so we need it)
void lrot(node* P){
  node* W = P->left;
  node* X = W->right;

  //W->left remains same
  //W->right becomes X->left
  W->right = X->left;

  //X->left becomes W
  X->left=W;

  //Parent node's new left child becomes X
  P->left=X;
  //X->right stays same same
}

//P is the parent of the rotation point (we don't store parent pointer, so we need it)
void rrot(node* P){
  node* X = P->left;
  node* W = X->left;

  //X->left becomes W->right
  X->left=W->right;

  //W->left remains same

  //W->right becomes X
  W->right = X;


  //Parent node's new left child becomes W
  P->left=W;
  //X->right stays same same
}

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
  node *p=root, *g=NULL, *o = root->left->right;
  visit(root);
  while (o) {
    if (o->left) { // if o has a child, o pulls p
      lrot(p); // pull(o,p);
      g=p;
      p=o;
      o = o->left->right;
    } else {
      if (p == root) { // if p is the root, o pulls p
        /* pull(o,p); */
        lrot(p); // pull(o,p);
      } else { // otherwise, g pulls p and root pulls p
        rrot(g);
        assert(p->left && (p->left->left == NULL));
        node* tmp=root->left;

        root->left = p->left;
        p->left=p->left->right;
        root->left->right=tmp;
        /* pull(root,p); */
        p=root; //g could be set to null
      }
      o = o->right;
    }
    visit(root);
  }
}
int main(int argc, char **argv) { coolBintree(atoi(argv[1])); }
