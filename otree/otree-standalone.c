#include <stdio.h>
#include <stdlib.h>

// ordered tree struct with pointers to parent, first child, and right sibling
typedef struct node { 
  struct node *parent, *first, *right; 
} node;


// prints ordered tree as a Dyck word; does not print newline
void visitrec(node* n){
  node* child = n->first;
  while(child){
    putchar('1');
    visitrec(child);
    child = child->right;
    putchar('0');
  }
}
// prints ordered tree as Dyck word with newline
void visit(node* n){ 
  visitrec(n); 
  putchar('\n');
}

// A pulls B:
// i.e. B's first child is removed from B's list of children and prepended to A's list of children
void pull(node *A, node *B){
  node *pulled = B->first;
  B->first = pulled->right;
  pulled->right = A->first;
  A->first = pulled;
  pulled->parent = A;
}

void coolOtree(int n) {
  // initialization: get tree where root has 2 children, 
  // root's second child is a path of length (n-2)
  node* root = (node*)calloc(sizeof(node),1);
  node* curr = root;
  for(int i = 0; i < n; i++){
    curr->first = (node*)calloc(sizeof(node),1);
    curr->first->parent=curr;
    curr=curr->first;
  }
  pull(root,curr->parent);
  node *o = root->first->right; // o starts as root's second child
  node *p = root; // p starts as root

  visit(root); // visit first tree

  while (o) { // main loop: run as long as O is nonnull
    p=o->parent;
    if (o->first) { // if p is the root, o pulls p
      pull(o,p);
      o = o->first->right;
    } else {
      if (p == root) { // if p is the root, o pulls p
        pull(o,p);
      } else { // otherwise, g pulls p and root pulls p
        pull(p->parent,p);
        pull(root,p);
      }
      o = o->right;
    }
    visit(root);
  }
}

int main(int argc, char **argv) { 
  if(argc > 1)
    coolOtree(atoi(argv[1])); 
  else{
    printf("usage: ./otree n\n");
    printf("generates all ordered trees with n nodes\n");
  }
}
