#include "otree.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// A pulls B:
// i.e. B's first child is removed from B's list of children and prepended to A's list of children
void pull(node *A, node *B){
  node *pulled = B->first;
  B->first = pulled->right;
  pulled->right = A->first;
  A->first = pulled;
  pulled->parent = A;
}

void coolOtree(int t, void (*visit)(node *root)){
  node *root = get_initial_tree(t); // defined in otree-functions.c
  node *o = root->first->right;
  node *p = root;

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
  int t = 0;

  // void function that takes a node* as a parameter,
  // intended to visit the tree with the parameter node as its root
  void (*visit)(node* root) = print_tree_as_dyck;

  // parse arguments
  for (int i = 1; i < argc; i++) {
    if (argv[i][0] == '-') {
      int len = strlen(argv[i]);
      for (int j = 1; j < len; j++) {
        char argchar = argv[i][j];
        if (argchar == 'o') { // otree: print as tikz for ordered trees
          visit = print_otree_as_tikz;
        } else if (argchar == 'l') { // otree: print as lukasiewicz word
          visit = print_otree_as_luka;
        } else {
          fprintf(stderr, "Invalid argument -%c\n", argchar);
          exit(1);
        }
      }
    } else {
      // not exactly bulletproof
      t = atoi(argv[i]);
    }
  }

  if (t <= 0) {
    fprintf(stderr,
            "Missing/Invalid value for n: %d\nUsage: ./otree [args] n\n", t);
    exit(1);
  }

  coolOtree(t, visit);
}
