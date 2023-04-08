#include <stdio.h>
#include <stdlib.h>
typedef struct otreenode { struct otreenode *first; struct otreenode *right; } otreenode;

typedef struct bintreenode { struct bintreenode* left; struct bintreenode* right;} bintreenode;

#define OTREE_TO_BINTREE(n) ( (struct bintreenode*)((void*)(n->first)) )

inline void pull(otreenode *A, otreenode *B){ 
  otreenode *pulled = B->first;
  B->first = pulled->right;
  pulled->right = A->first;
  A->first = pulled;
}

void visitrec(otreenode* n){ 
  otreenode* child = n->first;
  while(child){
    putchar('1');
    visitrec(child);
    child = child->right;
    putchar('0');
  }
}

// Has an extra trailing zero for now (last leaf)...
void visit_bintree_rec(bintreenode* n){
  if (n == NULL){
    putchar('0');
    return;
  }else{
    putchar('1');
  }
  visit_bintree_rec(n->left);
  visit_bintree_rec(n->right);
}


void visit_otree(otreenode* n){ visitrec(n); putchar('\n');}
void visit_bintree(bintreenode* n){ visit_bintree_rec(n); putchar('\n'); }

void coolOtree(int n) {
  otreenode *root = (otreenode*)calloc(sizeof(otreenode),1);
  otreenode *prev, *curr = root;
  for(int i = 0; i < n; i++){
    curr->first = (otreenode*)calloc(sizeof(otreenode),1);
    prev=curr;
    curr=curr->first;
  }
  pull(root,prev);
  otreenode *p=root, *g=NULL, *o = root->first->right;
  /* visit_otree(root); */
  visit_bintree(OTREE_TO_BINTREE(root));
  while (o) {
    if (o->first) { // if o has a child, o pulls p
      pull(o,p);
      g=p;
      p=o;
      o = o->first->right;
    } else {
      if (p == root) { // if p is the root, o pulls p
        pull(o,p);
      } else { // otherwise, g pulls p and root pulls p
        pull(g,p);
        pull(root,p);
        p=root;
      }
      o = o->right;
    }
    /* visit_otree(root); */
    visit_bintree(OTREE_TO_BINTREE(root));
  }
}

int main(int argc, char **argv) { coolOtree(atoi(argv[1])); }
