#include "luka.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// one pointer update
node *popchild(node *nod) {
  node *result = nod->left_child;
  nod->left_child = result->right_sibling;
  return result;
}

// 3 pointer updates
void pushchild(node *parent, node *child) {
  child->right_sibling = parent->left_child;
  parent->left_child = child;
  child->parent = parent;
}

// versions that maintain the left_sibling pointer (binary tree parent)
node *popchild_flex(node *nod) {
  node *result = nod->left_child;
  node *rsib = result->right_sibling;
  nod->left_child = rsib;
  if (rsib) {
    rsib->left_sibling = NULL;
  }
  return result;
}
void pushchild_flex(node *parent, node *child) {
  node *rsib = parent->left_child;
  child->right_sibling = rsib;
  if (rsib) {
    rsib->left_sibling = child;
  }
  parent->left_child = child;
  child->parent = parent;
}

// a mess, but good for coloring nodes
int mark(node *root, node *o, node **marked_nodes) {
  /* fancy_otree_tikz(root); */
  /* fprintf(stderr,"mark:  "); */
  if (o) {
    o->data = -1;
    /* fprintf(stderr," o"); */
    /* fprintf(stderr," %p",o); */
    marked_nodes[0] = o;
    node *p = o->parent;
    if (p) {
      p->data = -2;
      /* fprintf(stderr," p"); */
      /* fprintf(stderr," %p",p); */
      marked_nodes[1] = p;
      node *l = p->left_child;
      l->data = -3;
      /* fprintf(stderr," l"); */
      /* fprintf(stderr," %p",l); */
      marked_nodes[2] = l;
      node *g = p->parent;
      if (g) {
        /* fprintf(stderr," g"); */
        /* fprintf(stderr," %p",g); */
        /* fprintf(stderr," g"); */
        g->data = -4;
        marked_nodes[3] = g;
        /* fprintf(stderr,"\ng is %p",marked_nodes[3]); */
      }
    }
  }
  /* fprintf(stderr,"\n"); */
}

void unmark(node **marked_nodes) {
  /* fprintf(stderr,"unmark:"); */
  for (int i = 0; i < N_MARKED; i++) {
    if (marked_nodes[i]) {
      /* printf("%d %p\n",i,marked_nodes[i]); */
      /* fprintf(stderr," %p",marked_nodes[i]); */
      marked_nodes[i]->data = 0;
    }
  }
  /* fprintf(stderr,"\ng is %p",marked_nodes[3]); */
  /* fprintf(stderr,"\n\n"); */
}

void coolOtreeMarking(int t, void (*visit)(node *root),
                      void (*push)(node *parent, node *child),
                      node *(*pop)(node *child)) {
  node *root = get_initial_tree(t); // defined in otree-functions.c
  node *o = root->left_child->right_sibling;

  node *marked_nodes[N_MARKED] = {NULL};
  /* bzero(marked_nodes,N_MARKED * sizeof(node*)); */

  while (o) {
    mark(root, o, marked_nodes);
    visit(root);
    if (o->left_child) { // if o has a child, shift 1
      push(o, pop(o->parent));
      o = o->left_child->right_sibling;
    } else {
      if (o->parent == root) { // if the string is tight, shift a 1
        push(o, pop(o->parent));
      } else { // if the string isn't tight, shift a zero
        node *p = o->parent;
        push(p->parent, pop(p));
        push(root, pop(p));
      }
      o = o->right_sibling;
    }
    visit(root);
    unmark(marked_nodes);
    printf("\n\n");
  }
}

int diffluka(ll_node *a, ll_node *b) {
  while (a && b) {
    if (a->data - b->data) {
      return a->data - b->data;
    }
    a = a->next;
    b = b->next;
  }
  if (a || b) {
    return -1;
  }
  return 0;
}

void getnodes(ll_node *hd, ll_node **fptr, ll_node **optr, ll_node **pptr,
              ll_node **gptr) {
  ll_node *curr = hd;
  ll_node *p = NULL;
  ll_node *g = NULL;
  while (curr->data != 0) {
    if (curr->data >= 2) {
      p = curr;
      g = p->prev;
    }
    curr = curr->next;
  }
  *fptr = curr;
  *optr = curr->next;
  *pptr = p;
  *gptr = g;
}

ll_node* get_initial_luka(int t){
    ll_node* hd = new_llnode(2,NULL,NULL);
    ll_node* curr = new_llnode(0,hd,NULL);
    hd->next=curr;
    
    for(int i = 0; i < t-2; i++){
	curr->next=new_llnode(1,curr,NULL);	
	curr->next->prev=curr;
	curr=curr->next;
    }

    //we need the final leaf 0
    curr->next=new_llnode(0,curr,NULL);
    curr->next->prev=curr;

    return hd;
}

void coolOLuka(int t) {
    ll_node *lf, *lo, *lp, *lg;
    ll_node *hd = get_initial_luka(t);
    lf=hd->next;
    lo=lf->next;
    lp=hd;
    lg=NULL;

    print_ll(hd);
    while (lo) {
	if (lo->data) { // if o has a child, shift 1

	    lf->next = lo->next;
	    lo->next = lp->next;
	    lp->next = lo;
	    lp->data--;
	    lo->data++;

	    lg = lp;
	    lp = lo;
	    lo = lf->next;
	} else {
	    if (lp == hd) { // if the string is tight, shift a 1

		lf->next = lo->next;
		lo->next = lp->next;
		lp->next = lo;
		lp->data--;
		lo->data++;

		lg = NULL;
		lp = lp;
		lo = lf->next;
	    } else { // if the string isn't tight, shift a zero

		lg->data++;
		lp->data--;
		lf->next = lp; // lf->next=o;
		lg->next = lp->next;
		lp->next = lo;
		hd->data++;

		lp->data--;
		lp->next = lo->next; // works because o has no children
		lo->next = hd->next;
		hd->next = lo;

		lg = NULL;
		lp = hd;
		lf = hd->next;
		lo = lf->next;
	    }
	}
	print_ll(hd);

    }
}

void coolOtree(int t, void (*visit)(node *root),
               void (*push)(node *parent, node *child),
               node *(*pop)(node *child)) {
  node *root = get_initial_tree(t); // defined in otree-functions.c
  node *o = root->left_child->right_sibling;

  visit(root);

  while (o) {
    if (o->left_child) { // if o has a child, shift 1
      push(o, pop(o->parent));
      o = o->left_child->right_sibling;
    } else {
      if (o->parent == root) { // if the string is tight, shift a 1
        push(o, pop(o->parent));
      } else { // if the string isn't tight, shift a zero
        node *p = o->parent;
        push(p->parent, pop(p));
        push(root, pop(p));
      }
      o = o->right_sibling;
    }
    visit(root);
  }
}

int main(int argc, char **argv) {
  // not exactly bulletproof
  /* coolOtree(atoi(argv[1]), print_tree_as_dyck); */

  int t = 0;

  // void function that takes a node* as a parameter,
  // intended to visit the tree with the parameter node as its root
  void (*visit)(node * root) = print_tree_as_dyck;

  // void function that takes an int and a visiting function (like the one
  // above) as paremeters
  void (*generate)(int t, void (*visit)(node *), void (*push)(node *, node *),
                   node *(*pop)(node *)) = coolOtree;
  void (*push)(node *, node *) = pushchild;
  node *(*pop)(node *) = popchild;

  // parse arguments
  for (int i = 1; i < argc; i++) {
    if (argv[i][0] == '-') {
      int len = strlen(argv[i]);
      for (int j = 1; j < len; j++) {
        char argchar = argv[i][j];
        if (argchar == 'b') { // bintree: print as tikz for binary tree
          visit = print_bintree_as_tikz;
        } else if (argchar == 'o') { // otree: print as tikz for ordered trees
          visit = print_otree_as_tikz;
        } else if (argchar == 'l') { // otree: print as lukasiewicz word
          visit = print_otree_as_luka;
        } else if (argchar == 'k') { // otree: print as tikz for ordered trees
          generate = coolOLuka;
        } else if (argchar == 'f') { // flexible: maintain parent pointer for
                                     // binary tree (right_sibling)
          push = pushchild_flex;
          pop = popchild_flex;
        } else if (argchar == 'v') { // otree: print as tikz for ordered trees
          generate = coolOtreeMarking;
          visit = fancy_otree_tikz;
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

  generate(t, visit, push, pop);
}
