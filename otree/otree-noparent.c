#include <stdio.h>
#include <stdlib.h>
typedef struct node { struct node *first; struct node *right; } node;

void pull(node *A, node *B){ 
  node *pulled = B->first;
  B->first = pulled->right;
  pulled->right = A->first;
  A->first = pulled;
}

void visitrec(node* n){ //prints an ordered tree as a dyck word;
  node* child = n->first;
  while(child){
    putchar('1');
    visitrec(child);
    child = child->right;
    putchar('0');
  }
}
void visit(node* n){ visitrec(n); putchar('\n');}
/* void visit(node* n){ return;} */

void coolOtree(int n) {
  node *root = (node*)calloc(sizeof(node),1);
  node *prev, *curr = root;
  for(int i = 0; i < n; i++){
    curr->first = (node*)calloc(sizeof(node),1);
    prev=curr;
    curr=curr->first;
  }
  pull(root,prev);
  node *p=root, *g=NULL, *o = root->first->right;
  visit(root);
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
        p=root; //g could be set to null
      }
      o = o->right;
    }
    visit(root);
  }
}
int main(int argc, char **argv) { coolOtree(atoi(argv[1])); }
