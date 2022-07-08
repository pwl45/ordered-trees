#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "aotree.h" 

anode* apopchild(anode* nod){
  return nod->children[nod->nch--];
}

void apushchild(anode* parent, anode* child){
  parent->children[++parent->nch]=child;
  child->parent=parent;
}

void apull(anode* A, anode* B){ 
  //A pulls B's first child
  anode* pulled = B->children[B->nch--];
  A->children[++(A->nch)]=pulled;
  pulled->parent=A;
}

anode* kthchild(anode* parent, int k){
  return parent->children[parent->nch-k+1];
}

//get the tree corresponding to 101^{t-1}0^{t-1}
anode* get_initial_atree(int t){
  anode* root = new_anode(t);
  anode* curr=root;
  for(int i = 0; i < t; i++){
    apushchild(curr,new_anode(t));
    curr=kthchild(curr,1);
  }
  apull(root,curr->parent);
  return root;
}


void coolAOtree(int t, void (*visit)(anode*)){
  anode* root = get_initial_atree(t);
  anode *p, *o=kthchild(root,2);
  visit(root);
  while(o){
    p = o->parent;
    if(kthchild(o,1)){ //if o has a child, shift 1
      apull(o,p);
      o=kthchild(o,2);
    }else{
      if(p == root){ //if the string is tight, shift a 1
	apull(o,p);
      }else{ //if the string isn't tight, shift a zero
	apull(p->parent,p);
	apull(root,p);
      }
      o=kthchild(o->parent,2);
    }
    visit(root);
  }
}

int main(int argc, char** argv){
  //not exactly bulletproof
  /* printf("aotree\n"); */
  if(argc < 2)
    exit(1);

  coolAOtree(atoi(argv[1]), print_atree_as_dyck);
}
