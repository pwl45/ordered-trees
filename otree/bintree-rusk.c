#include <stdio.h>
#include <stdlib.h>
typedef struct node { struct node *left; struct node *right; struct node* parent;} node;
typedef struct bintreenode { struct bintreenode* left; struct bintreenode* right;} bintreenode;

// Has trailing zero for now
void visit_bintree_rec(node* n){
  if (n == NULL){
    putchar('0');
    return;
  }else{
    putchar('1');
    // make sure parent pointers are good
    if((n->left && n->left->parent != n) || (n->right && n->right->parent != n)){
      exit(1);
    }
  }
  visit_bintree_rec(n->left);
  visit_bintree_rec(n->right);
}

void visit(node* root){ visit_bintree_rec(root); putchar('\n');}

void coolBintree(int n) {
  node *curr;
  node* R=(node*)calloc(sizeof(node),1);
  if (n>=2){
    R->right=calloc(sizeof(node),1);
    R->right->parent=R;
  }
  if(n >= 3){
    curr=R->right;
    for(int i = 2; i < n; i++){
      curr->left = (node*)calloc(sizeof(node),1);
      curr->left->parent=curr;
      curr=curr->left;
    }
  }
  node *x = R->right, *y=R;

  visit(R);
  while (x) {
    if (x->left) { // Case (a) in Ruskey and Williams
      y->right = x->right;
      y->right && (y->right->parent=y);

      x->right = x->left;
      //no parent change needed

      x->left = y->left;
      (x->left) && (x->left->parent = x);

      y->left = x;
      (y->left) && (y->left->parent = y);

      y=x;
      x=y->right;
    } else {
      if(R==y){ // Case (c) in Ruskey and Williams
        x->left=y;
        x->left->parent=x;

        y->right=NULL;
        // no parent change needed

        R=x;

        y=x;
        x=x->right;
        R->parent=NULL;
      } else { // Case (b) in Ruskey and Williams
        // l(p(y)) <- l(y)
        y->parent->left = y->left; //1
        y->parent->left && (y->parent->left->parent = y->parent); //2

        // l(x) <- r(x)
        x->left=x->right; //3
        //no parent change needed x->right already has x as its parent

        // r(x) <- r(p(y))
        x->right=y->parent->right; //4
        y->parent->right && (y->parent->right->parent=x); //5

        // r(p(y)) <- x
        y->parent->right = x; //6
        x->parent=y->parent; //7


        // l(y) <- nil
        y->left=NULL; //8
        // no parent change needed: NULL doesn't need a parent

        // r(y) <- R
        y->right=R; //9
        R->parent=y; //10

        // R <- y
        R=y; //11
        R->parent=NULL; //12

        // x <- r(y)
        x=y->right; //13
      }

    }
    visit(R);
  }
}
int main(int argc, char **argv) { coolBintree(atoi(argv[1])); }
