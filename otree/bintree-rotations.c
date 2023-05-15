#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct node { struct node *left; struct node *right; char* data;} node;
typedef struct bintreenode { struct bintreenode* left; struct bintreenode* right;} bintreenode;

//if B is null, root is being pulled, so new root is old root's right child
//if A is null, pulled becomes the new root
node* pull(node* root, node *A, node *B){ 
  node* pulled = (B ? B->left : root);
  node* pulledright=pulled->right;
  B && (B->left=pulled->right);
  pulled->right= (A ? A->left : root);
  A && (A->left=pulled);
  return (B&&A) ? root : (A ? pulledright : pulled);
  /* if(B&&A){ */
  /*   return root; */
  /* }else if(A){ */
  /*   return A; */
  /* }else if(B){ */
  /*   return pulled; */
  /* } */
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


void bintree(node* n){
  if(n == NULL){
    // Empty node
    printf("\\edge[draw=none]; \\node[blank]{}; ");
    return;
  }
  if(n->data){
    printf("[.{%s}\n",n->data);
  }else{
    printf("[.{} ");
  }
  /* if(n->data==1){ */
  /*   printf("[.{O} "); */
  /* }else if(n->data==2){ */
  /*   printf("[.{P} "); */
  /* }else if(n->data=='A'){ */
  /*   printf("[.{A} "); */
  /* }else if(n->data=='B'){ */
  /*   printf("[.{A} "); */
  /* }else{ */
  /*   printf("[.{} "); */
  /* } */

  bintree(n->left);
  bintree(n->right);
  printf("] ");
}

void print_bintree_as_tikz(node* n){
  printf("\\begin{tikzpicture}[every tree node/.style={draw,circle},sibling distance=10pt, level distance=40pt]\n\\tikzset{every tree node/.style={minimum width=1.5em,draw,circle}, blank/.style={draw=none}, edge from parent/.style= {draw,edge from parent path={(\\tikzparentnode) -- (\\tikzchildnode)}}, level distance=1.5cm}\n\\Tree");
  bintree(n);
  printf("\n\\end{tikzpicture}\\hspace{1.5em}\n");
  printf("\n");
}

// otree root->left is start of binary tree
/* void visit(node* root){ visit_bintree_rec(root->left); putchar('\n');} */
void visit(node* root){ visit_bintree_rec(root); putchar('\n');}

int d2brec(node* root, char* w, int i, int len, int left){
  if(i>=len){
    return len;
  }
  if(w[i]=='1' || w[i]==1){
    node* curr = (node*)calloc(sizeof(node),1);
    root->left=curr;
    int off = d2brec(curr,w,i+1,len,1)+1;
    if(off >= len){
      return off;
    }
    if (w[off]=='1' || w[off]==1){
      curr = (node*)calloc(sizeof(node),1);
      root->right=curr;
      int off2 = d2brec(curr,w,off+1,len,1);
      return off2;
    }else{
      return off;
    }
  }else{
    root->left=NULL;
    i+=1;
    if(i>=len){
      return len;
    }
    if(w[i]=='1' || w[i]==1){
      node* curr = (node*)calloc(sizeof(node),1);
      root->right=curr;
      int off=d2brec(curr,w,i+1,len,1);
      return off;
    }else{
      root->right=NULL;
      return i;
    }
  }
}

node* d2b(char* w){
  node* root = (node*)calloc(sizeof(node),1);
  d2brec(root,w,0,strlen(w),1);
  return root;
}

void coolOtree(int n) {
  node *root = (node*)calloc(sizeof(node),1);
  node *prev, *curr = root;
  for(int i = 0; i < n; i++){
    curr->left = (node*)calloc(sizeof(node),1);
    prev=curr;
    curr=curr->left;
  }
  root=pull(root,root,prev);
  node *p=NULL, *g=NULL, *o = root->left->right;
  root=root->left;
  int i=0;
  print_bintree_as_tikz(root);
  while (o && i<200) {
    i++;
    if (o->left) { // if o has a child, o pulls p
      printf("Pull O P \\pagebreak \n\n");
      root=pull(root,o,p);
      o&&(o->data="O");
      p&&(p->data="P");
      g=p;
      p=o;
      o = o->left->right;
    } else {
      if (p == NULL ) { // if p is the root, o pulls p
        printf("Pull O P \\pagebreak \n\n");
        root=pull(root,o,p);
        o&&(o->data="O");
        p&&(p->data="P");
      } else { // otherwise, g pulls p and root pulls p
        printf("Double Pull: g pull p\n\n");

        root=pull(root,g,p);
        print_bintree_as_tikz(root);
        printf("root pull p \n\n");
        root=pull(root,NULL,p);
        printf("\\pagebreak\n");
        o&&(o->data="O");
        p&&(p->data="P");
        p=NULL; //g could be set to null
      }
      o = o->right;
    }
    p&&(p->data="P");
    o&&(o->data="O");
    print_bintree_as_tikz(root);
    /* o&&(o->data=0); */
    /* p&&(p->data=0); */
  }
}

//A above B:
//A
int main(int argc, char **argv) { 
  node* root = d2b("11111100101001111001001001100010010110010");

  // pull(x,x->left) <=> rotateright(x)
  /* node* A=root->left->left->left; */
  /* node* B=A->left; */

  /* // pull(x->left->right,x) <=> rotateleft(x) */
  /* node* B=root->left->left->left; */
  /* node* A=B->left->right; */

  // General Pull Example
  node* A=root->left;
  node* B=root->left->left->left->left->right;

  B->data="B";
  B->left->data="X";
  /* B->left->right->data="X"; */
  (B->left->right)&&(B->left->right->data="Y");
  A->data="A";
  print_bintree_as_tikz(root);
  pull(root,A,B);
  print_bintree_as_tikz(root);
  /* coolOtree(atoi(argv[1])); */ 
}
