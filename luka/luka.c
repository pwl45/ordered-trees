#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
//Generates all Lukasiewicz words with a given set of content, 
//generating each Lukasiewicz word in worst-case O(1) time
// - Uses a (doubly) linked list reprseentation of a Lukasiewicz word to allow for O(1) left-shifts
// - Keeps track of prefix_sum and a stack of all increases in the string to avoid scanning string
//See luka_ll for the main generating function

/* -----------------------Variables for coloring terminal output----------------------- */
const char* increase_colors[] = {"\033[31m", "\033[32m", "\033[34m", "\033[33m", "\033[35m", "\033[36m"};
const char* RESET = "\033[0m";
int ncolors = sizeof(increase_colors)/sizeof(char*);

//linked list node struct
typedef struct ll_node {
  int data;
  struct ll_node* prev;
  struct ll_node* next;
} ll_node;
//inc struct for keeping track of linked list increases
typedef struct inc {
  struct ll_node* node;
  int index;
} inc;

//initialize ll_node
ll_node* new_node(int data, ll_node* prev, ll_node* next){
  ll_node* node = (ll_node*) malloc(sizeof(ll_node*));
  node->data=data;
  node->prev=prev;
  node->next=next;
  return node;
}

/* ---------------------------------PRINTING FUNCTIONS--------------------------------- */
/* Called by visiting functions*/
//basic function to print list
void print_ll(ll_node* hd){
  printf("[");
  if(hd){
    printf("%d",hd->data);
  }
  while( (hd=hd->next) ){
    printf(", %d",hd->data);
  }
  printf("]");
  printf("\n");
}

// Prints arrow to visualize a shift
// note: double digit numbers will break this (arrows will be wrong length).
// Not especially robust, but nice for basic visualizations.
void print_arrow(int to_index, int from_index){
  to_index = 1+3*(to_index);
  from_index = 1+3*(from_index);
  for(int i = 0; i < from_index+1; i++){
    if(i < to_index){
      putchar(' ');
    }
    else if(i == to_index || i == from_index){
      putchar('|');
    }
    else if(i == to_index+1){
      putchar('<');
    }else{
      putchar('-');
    }
  }
  putchar('\n');
}

void print_ll_rainbow(ll_node* hd, int n, ll_node* x){
  printf("[");
  if(hd){
    printf("%d",hd->data);
  }
  int incno = 0;
  while( (hd=hd->next) ){
    if(hd == x){
      printf(", \033[31;1;4m%d\033[0m",hd->data);
      incno++;
    }else if (hd->prev && hd->data > hd->prev->data){
      printf(", %s%d%s",increase_colors[incno%ncolors],hd->data,RESET);
      incno++;
    }else{
      printf(", %d",hd->data);
    }
  }
  printf("]");
  printf("\n");
}
/* ------------------------------------------------------------------------------------ */


/* ---------------------------------VISITING FUNCTIONS--------------------------------- */
/* Each visiting function takes the following parameters:*/
/* - hd, a pointer to the head of the list */ 
/* - n, the length of the lists */
/* - incs, a pointer to a list of increases in the string */
/* - ninics, the number of increases in the string (length of incs) */
/* - prefix_sum, the sum of the non-increasing prefix of the string */
/* not every parameter will always to be used, but all must be provided */
/* Passing one of these visiting functions to luka_ll determines how each Lukasiewicz word is outputted*/

//Basic function to print a Lukasiewicz word
void visit_ll_basic(ll_node* hd, int n, inc* incs, int nincs, int prefix_sum){
  print_ll(hd);
}

// Print a Lukasiewicz word with each increase colored (and the first increase underlined/bolded
void visit_ll_rainbow(ll_node* hd, int n, inc* incs, int nincs, int prefix_sum){
  if(nincs){
    print_ll_rainbow(hd,n,incs[nincs-1].node); //node at index m+1
  }else{
    print_ll(hd);
  }
}

//Print a Lukasiewicz word with colors and use arrows to illustrate each left-shift.
void visit_ll_visual(ll_node* hd, int n, inc* incs, int nincs, int prefix_sum){
  int to_index = -1;
  int from_index = -1;
  if(nincs){
    ll_node* shift_node = NULL;
    int m = incs[nincs-1].index;
    ll_node* x=incs[nincs-1].node; //node at index m+1
    print_ll_rainbow(hd,n,x);
    if(m >= n-1 || x->prev->data < x->next->data || (x->next->data == 0 && prefix_sum == m)){
      shift_node=x;
      from_index = m;
    }
    else{
      from_index = m+1;
      shift_node=x->next;
    }
    to_index = !shift_node->data;
    print_arrow(to_index,from_index);
  }else{
    print_ll(hd);
  }
}
/* ------------------------------------------------------------------------------------ */

/* ------------------------------ Left-shifting Function ------------------------------ */
//Implementation of the left-shfting operation in a linked list.
// shift_node is shifted in front of insert_node
void lshift(ll_node* insert_node, ll_node* shift_node){
  //remove shift_node
  ll_node* sprev=shift_node->prev;
  ll_node* snext=shift_node->next;
  sprev->next=snext;
  if(snext)
    snext->prev=sprev;

  //insert shift_node before insert_node
  ll_node* iprev=insert_node->prev;
  shift_node->prev=iprev;
  if(iprev)
    iprev->next=shift_node;

  shift_node->next=insert_node;
  insert_node->prev=shift_node;
}


/* ------------------------------Main Generating Function------------------------------ */
//Generates all Lukasiewicz words with a given set of content
//uses visit function pointer to allow for different methods of output
//Assumes input string is sorted in descending order.  
//hd: head of list 
//n: length of list; 
//visit: function called on each generated Lukasiewicz word (used for outputting results).
void luka_ll(ll_node* hd, ll_node* tl, int n, void (*visit)(ll_node* hd, int n, inc* incs, int nincs, int prefix_sum)){
  inc* incs = (inc*) calloc(n, sizeof(inc)); //stack of (node, index) pairs; tracks every increase in the string
  int nincs=1; //number of increases

  ll_node *shift_node, *insert_node, *x, *xn;
  int prefix_sum,m,insert_index;

  incs[0] = (inc) {.node=tl,.index=n-1};

  while(nincs){
    m = incs[nincs-1].index;
    x=incs[nincs-1].node; //node at index m+1
    xn=x->next; //node at index m+2

    //Determine which index to shift from, and if that shift will add/remove an increase
    if(m >= n-1 || xn->data > x->prev->data || (prefix_sum == m && xn->data == 0)){ //shift from index m+1
      shift_node=x; //x is the node at index m+1
      if(m >= n-1 || xn->data > x->data || xn->data == 0){ //increase removed by shifting 
        nincs--;
      }else{ //increase maintained, but is now one further down the string
        incs[nincs-1].node=x->next;
        incs[nincs-1].index++;
      }
    }
    else{ //shift from index m+2
      shift_node=xn; //xn is the node at index m+2
      incs[nincs-1].index++;
      if(xn->next && xn->next->data > xn->data && xn->next->data <= x->data){
        incs[nincs-2] = incs[nincs-1];
        nincs--;
      }
    }

    insert_node=hd->next;
    
    insert_index=!(shift_node->data); //if shifted value is 0, shift to index 1. otherwise, to index 0.
    if(!insert_index){ //update head if shifting to position 0
      insert_node=hd;
      hd=shift_node;
    }

    lshift(insert_node,shift_node); //execute shift
    if(insert_index != m && (shift_node->data < insert_node->data)){ 
      //check if we created an increase at the front of the string
      prefix_sum=hd->data;
      incs[nincs++]= (inc) {.node = insert_node, .index=insert_index+1};
    }else{
      //otherwise, increase prefix_sum by the value we shifted
      prefix_sum+=shift_node->data;
    }
    visit(hd,n, incs, nincs,prefix_sum);

  }
  free(incs);
}
/* ------------------------------------------------------------------------------------ */

/* ----------------Code for reading input and constructing initial list---------------- */
// not especially well written, but good enough for now
ll_node* append_ll(ll_node* tl, int val,int freq){
  ll_node* newtl;
  for(int i = 0; i < freq; i++){
    newtl = new_node(val, tl,NULL);
    newtl->prev=tl;
    tl->next=newtl;
    tl=newtl;
  }

  return tl;
}
ll_node* prepend_ll(ll_node* hd, int val,int freq){
  ll_node* newhd;
  for(int i = 0; i < freq; i++){
    newhd = new_node(val, NULL,hd);
    hd->prev=newhd;
    hd=newhd;
  }

  return hd;
}
//reads comma separated frequency list, e.g. 2,3,0,1 means 2 zeroes, 3 ones, 0 twos, and 1 three.
//will certainly seg fault if given invalid input
int read_input_ll(char* frequencies, int* nptr, ll_node** hdptr, ll_node** tlptr){
  const char delim[2] = ","; //[2] because of null
  char* token = strtok(frequencies, delim);

  int i=0;
  //skip until we find a non-zero frequency
  while(atoi(token) == 0){
    token=strtok(NULL, delim);
    i++;
  }

  //we know we're at a non-zero frequency, use it to start our list
  ll_node* hd = new_node(i,NULL,NULL);
  ll_node* tl = hd;
  int freq = atoi(token);
  tl=append_ll(tl,i,freq-1);

  token = strtok(NULL, delim);
  int n=freq;
  i++;
  while(token){
    int freq = atoi(token);
    if(freq){
      hd = prepend_ll(hd, i,freq);
    }
    i++;
    n+= freq;
    token = strtok(NULL, delim);
  }

  *hdptr=hd;
  *tlptr=tl;
  *nptr=n;
  return 0;
}
/* ------------------------------------------------------------------------------------ */


void print_usage(){
  printf("usage: ./luka frequencies [options]\n");
  printf("For example, run ./luka 3,1,1,1 for all Lukasiewicz words with content {0,0,0,1,2,3}\n");
  printf("By default, the 'first increase' is colored red and underlined.  subsequent increases are colored with other colors.\n");
  printf("Options:\n");
  printf("  -n: no color; turn off colored output\n");
  printf("  -v: 'visualize' left-shifts (with arrows)\n");
  exit(1);
}

int main(int argc, char *argv[])
{
  int n;
  ll_node *hd,*tl;
  void (*visit)(ll_node* hd, int n, inc* incs, int nincs, int prefix_sum) = visit_ll_rainbow;
  if(argc < 2 || strcmp(argv[1],"-h") == 0){
    print_usage();
    exit(1);
  }else if(argc >= 3){
    for(int i = 2; i < argc; i++){
      if(strcmp(argv[i],"-v") == 0){
        visit = visit_ll_visual;
      }
      else if(strcmp(argv[i],"-n") == 0){
        visit = visit_ll_basic;
      }else{
        printf("Unrecognized argument %s\n",argv[i]);
        print_usage();
        exit(1);
      }
    }
  }

  read_input_ll(argv[1], &n, &hd, &tl);

  luka_ll(hd,tl,n,visit);
  //should theoretically free everything in the linked list...

  return 0;
}
