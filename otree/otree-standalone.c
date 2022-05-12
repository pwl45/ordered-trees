#include <stdio.h>
#include <stdlib.h>
typedef struct node { struct node *parent, *first, *right; } node;

void pull(node *A, node *B){ // A pulls B's first child
  node *pulled = B->first;
  B->first = pulled->right;
  pulled->right = A->first;
  A->first = pulled;
  pulled->parent = A;
}

void visit(node* root){ //prints an ordered tree as a dyck word
  node* child = root->first;
  while(child){
    putchar('1');
    visit(child);
    child = child->right;
    putchar('0');
  }
  if(!root->parent) putchar('\n');
}

node* kthchild(node* parent, int k){
  node* curr=parent->first;
  for(int i = 1; i < k; i++){
    curr=curr->right;
  }
  return curr;
}

void coolOtree(int n) {
  node* root = (node*)calloc(sizeof(node),1);
  node* curr = root;
  for(int i = 0; i < n; i++){
    curr->first = (node*)calloc(sizeof(node),1);
    curr->first->parent=curr;
    curr=curr->first;
  }
  pull(root,curr->parent);
  node *p, *o = kthchild(root,2);
  visit(root);
  while (o) {
    p=o->parent;
    if (o->first) { // if o has a child, shift 1
      pull(o,p);
      o = kthchild(o,2);
    } else {
      if (p == root) { // if the string is tight, shift a 1
        pull(o,p);
      } else { // if the string isn'n tight, shift a zero
        pull(p->parent,p);
        pull(root,p);
      }
      o = kthchild(o->parent,2);
    }
    visit(root);
  }
}

int main(int argc, char **argv) { coolOtree(atoi(argv[1])); }
