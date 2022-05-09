#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>



uint64_t sumshifts,nshifts;

//linked list node struct
typedef struct ll_node {
    char data;
    struct ll_node* prev;
    struct ll_node* next;
} ll_node;


//inc struct for keeping track of linked list increases
typedef struct inc {
    struct ll_node* node;
    int index;
} inc;

ll_node* new_node(int data, ll_node* prev, ll_node* next){
    ll_node* node = (ll_node*) malloc(sizeof(ll_node*));
    node->data=data;
    node->prev=prev;
    node->next=next;
    return node;
}

void write_ms(int *ms, int n){

}
void print_ms(int* ms, int n){
    /* printf("n=%d\n",n); */

    printf("[");
    if(n>=1){
	printf("%d",ms[0]);
    }
    for(int i = 1; i < n; i++){
	printf(", %d",ms[i]);
    }
    printf("]");
    printf("\n");
}

void write_ll(ll_node* hd, int n){
    char delm = -1;
    char buf[n+1];

    int i=0;
    while(hd){
	buf[i] = hd->data;
	hd=hd->next;
	i++;
    }
    buf[n]=delm;
    write(1,buf,n+1);
    /* write(1,&delm,1); */
}

void print_ll(ll_node* hd, int n){
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

void revprint_ll(ll_node* tl){
    printf("[");
    if(tl){
	printf("%d",tl->data);
    }
    while( (tl=tl->prev) ){
	printf(", %d",tl->data);
    }
    printf("]");
    printf("\n");
}

int sum(int* ms, int n){
    int sum=0;
    for(int i = 0; i < n; sum+=ms[i++]);
    return sum;
}

//atrocious code
int max(int* ms, int n){
    int max=0;
    for(int i=0; i < n; max = (ms[i++] > max) ? ms[i-1] : max);
    return max;
}

//will have to realloc a lot probably, oh well
int* append_ms(int* ms, int* n, int* sz, int val,int freq){
    
    int min=*n;
    int max=*n+freq;
    *n=max;
    if(*sz < *n){
	(*sz) = (*n);
	ms = (int*) realloc(ms,(*sz) * (sizeof(int)));
    }

    for(int i = min; i < max; i++){
	ms[i]=val;
    }

    return ms;
}

//funner way to swap things
void swap(int* a, int* b){
    *a ^= *b;
    *b ^= *a;
    *a ^= *b;
}

//reverses an  list of ints of length n
//a good for loop doesn't need a body
void rev(int* lo, int n){
    for(int* hi = lo + n - 1; hi > lo; swap((hi--),(lo++)));
}


//uses char* of frequencies to generate multiset
//not good code, but works. could be improved, but not that important.
int* initialize_ms(char* frequencies, int* nptr, int* maxptr){
    const char delim[2] = ","; //[2] because of null


    int sz = 100; //will be made smaller if necessary later
    int* ms = malloc(sizeof(int)*sz);
    int n=0;

    int i = 0;
    int max = 0;

    char* token = strtok(frequencies, delim);
    while(token){

	// this assignmment is necesary because realloc can change where ms starts
	int freq = atoi(token);
	if(freq){
	    ms = append_ms(ms, &n, &sz, i,freq);
	    max=freq;
	}
	i++;
	token = strtok(NULL, delim);
    }
    ms = realloc(ms,(n+1)*sizeof(int)); //give it size n+1

    *nptr=n;
    *maxptr=max;
    return ms;

}

void lshift(int* ms, int i, int j){
    /* nshifts++; */
    /* sumshifts+=(j-i); */
    /* printf("wah\n"); */
    /* if(!(nshifts & ((1<<20)-1) )){ */
	/* /1* printf("%lf\t%ld %ld\n",((double) sumshifts)/nshifts,sumshifts,nshifts/1000000); *1/ */
	/* /1* printf("rat: %lf\n",((double) sumshifts)/nshifts); *1/ */
    /* } */
    /* printf("%d\n",j-i); */
    int curr = ms[j];
    for(int k = i; k <= j; k++){
	swap(&curr,ms+ k);
    }

}

int stack_pop(int* stack, int *nptr){
    return stack[--(*nptr)];
}

void stack_push(int* stack, int *nptr, int val){
     stack[(*nptr)++] = val;
}

//this is slower but kind of fun. no if statements?
void dumb_luka(int* ms, int n, void (*visit)(int* ms, int n)){
    int prefix_len = n;
    int prefix_sum;
    int shift_index,insert_index;
    /* printf("max: %d\n",max(ms,n)); */
    /* exit(1); */
    int* incs = (int*) malloc(sizeof(int)*(n/2));
    int nincs = 1;
    incs[0]=n-1;
    while(nincs){
	prefix_len = incs[--nincs]++; //greedy increase of the first increase

	//this creates an increase, accounted for later.
	int shift1=((ms[prefix_len+1] <= ms[prefix_len-1]) & ((prefix_sum > prefix_len) | (ms[prefix_len+1]))) & (prefix_len < n-1);

	shift_index = prefix_len + shift1;
	insert_index = !ms[shift_index];
	/* printf("shift %d %d\n",insert_index,shift_index); */

	//these variables need to be named better
	int s1gtsminus = ms[shift_index+1] > ms[shift_index-1];
	int s1gts = (ms[shift_index+1] > ms[shift_index]);

	//did we create an increase at shift_index+1?
	int incnincs=((s1gtsminus) & (!s1gts)); // is & better than &&?

	//did we remove an increase at shift_index+1?
	int decincs=(!(s1gtsminus) & (s1gts));

	nincs+=incnincs+shift1-decincs;
	incs[nincs-1]-=decincs;


	lshift(ms,insert_index,shift_index);


	int incfront = (ms[insert_index] < ms[insert_index+1]) & (insert_index != prefix_len);

	incs[nincs]=insert_index+1;
	nincs+=incfront;
	prefix_sum = prefix_sum*!incfront + ms[0]*incfront;
	prefix_sum += ms[insert_index]*!incfront;


	visit(ms,n);
    }
}


void dprintnode(ll_node* n){
    if(n->prev){
	printf("(%d<-%d->",n->prev->data,n->data);
    }else{
	printf("([<-%d->",n->data);
    }
    if(n->next){
	printf("%d)\n",n->next->data);
    }else{

	printf("])\n");
    }
    /* printf("(%d<-%d->%d)\n",n->prev->data,n->data,n->next->data); */
}

void printincs(inc* incs, int nincs){
    printf("INCS:\n");
    printf("[");
    if(nincs>=1){
	printf("%d",incs[0].index);
    }
    for(int i = 1; i < nincs; i++){
	printf(", %d",incs[i].index);
    }
    printf("]\n");
    for(int i = 0; i < nincs; i++){
	dprintnode(incs[i].node);
    }
    printf("\n");
}

//TODO: i don't think we actually need the prev pointer. 
//Will need to pass the thing previous to the thing that needs to be shifted, though
void lshift_ll(ll_node* insert_node, ll_node* shift_node){
    //remove shift_node
    ll_node* sprev=shift_node->prev;
    ll_node* snext=shift_node->next;
    if(sprev){
	sprev->next=snext;
    }
    if(snext){
	snext->prev=sprev;
    }

    //insert shift_node before insert_node
    ll_node* iprev=insert_node->prev;
    shift_node->prev=iprev;
    if(iprev){
	iprev->next=shift_node;
    }

    shift_node->next=insert_node;
    insert_node->prev=shift_node;
}

ll_node* kthnode(ll_node* hd, int k){
    ll_node* curr=hd;
    while(k){
	curr=curr->next;
	k--;
    }
    return curr;
}

//TODO: we probably don't need tl, n, or a prev pointer.
void luka_ll(ll_node* hd, ll_node* tl, int n, void (*visit)(ll_node* hd, int n)){
    inc* incs = (inc*) calloc(n, sizeof(inc)); //stack of (node, index) pairs
    int nincs=1; //number of increases

    ll_node *shift_node, *insert_node, *x, *xn;
    incs[0] = (inc) {.node=tl,.index=n-1}; //cool struct initializer syntax
    int prefix_sum,m,insert_index;

    while(nincs){
	m = incs[nincs-1].index;
	x=incs[nincs-1].node; //node at index m+1
	xn=x->next; //node at index m+2

	if(m >= n-1 || xn->data > x->prev->data || (prefix_sum == m && xn->data == 0)){
	    if(m >= n-1 || xn->data > x->data || xn->data == 0){ //increase removed
		nincs--;
	    }else{ //increase kept
		incs[nincs-1].node=x->next;
		incs[nincs-1].index++;
	    }
	    shift_node=x;
	}
	else{ 
	    shift_node=xn; //shift x+1...
	    incs[nincs-1].index++;
	    if(xn->next && xn->next->data > xn->data && xn->next->data <= x->data){
		incs[nincs-2] = incs[nincs-1];
		nincs--;
	    }
	}

	insert_index=!(shift_node->data); //bang
	if(insert_index){
	    insert_node=hd->next;
	}else{
	    insert_node=hd;
	    hd=shift_node;
	}

	lshift_ll(insert_node,shift_node);
	if(insert_index != m && (shift_node->data < insert_node->data)){
	    prefix_sum=hd->data;
	    incs[nincs++]= (inc) {.node = insert_node, .index=insert_index+1};
	}else{
	    prefix_sum+=shift_node->data;
	}

	visit(hd,n);
    }
}

void luka(int* ms, int n, void (*visit)(int* ms, int n)){
    int prefix_len,prefix_sum,shift_index,insert_index;
    int* incs = (int*) calloc((n),sizeof(int));
    int nincs = 1;
    incs[0]=n;
    while(nincs){
	prefix_len = incs[nincs-1]++; //greedy increase of the first increase
	if(prefix_len >= n-1){
	    nincs--;
	    shift_index = n-1;
	    insert_index = !(ms[shift_index]); //nice bang
	}
	else if(ms[prefix_len+1] > ms[prefix_len-1]){
	    if(ms[prefix_len+1] > ms[prefix_len]){
		nincs--;
	    }
	    shift_index=prefix_len;
	    insert_index=0;
	}
	else{
	    if(prefix_sum > prefix_len || ms[prefix_len+1] > 0){
		shift_index = prefix_len+1;
		insert_index = !ms[shift_index];  //another nice bang
		//sentinel?
		if(prefix_len < n - 2 && ms[prefix_len+2] > ms[prefix_len+1] && ms[prefix_len+2] <= ms[prefix_len]){
		    //the rare triple minus
		    incs[nincs---2]--; // this could really be nincs--; incs[nincs-1]--;
		}
	    }else{
		nincs--;
		shift_index = prefix_len;
		insert_index = 0;
	    }
	}

	lshift(ms,insert_index,shift_index);

	if(ms[insert_index] < ms[insert_index+1]){
	    prefix_sum=ms[0];

	    if(insert_index != prefix_len){
		stack_push(incs,&nincs,insert_index+1); // can probably just inline this function later
	    }
	}else{
	    prefix_sum += ms[insert_index];
	}

	visit(ms,n);
    }
}

ll_node* append_ll(ll_node* tl, int val,int freq){
    ll_node* newtl;
    /* printf("append %d %d times\n",val,freq); */
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
    /* printf("prepend %d %d times\n",val,freq); */
    for(int i = 0; i < freq; i++){
	newhd = new_node(val, NULL,hd);
	hd->prev=newhd;
	hd=newhd;
    }

    return hd;
}

//not especially well written, good enough for now
ll_node* initialize_ll(char* frequencies, int* nptr){
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

    /* print_ll(hd); */
    /* revprint_ll(tl); */

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

    //temporarily make it a circle
    hd->prev=tl;
    *nptr=n;
    return hd;
}

void donothing(){

}

int main(int argc, char *argv[])
{
    if(argc < 2){
	printf("usage: ./luka frequencies [options]\n");
	printf("options are -a for array mode, anything else for linked-list mode.\n");
	exit(1);
    }

    int n;
    int max;
    if(argc >= 3 && !strcmp(argv[2],"-a")){ //robust argument handling
	//old array based approach
	int *ms = initialize_ms(argv[1],&n, &max);
	rev(ms,n);
	/* printf("%d %d\n",sum(ms,n),n); */
	/* exit(0); */
	ms[n]=666; //if we see 666 anywhere in the multiset, we've shifted from out of bounds.
	luka(ms,n,print_ms);
	/* printf("sum: %lu n: %lu\navg: %lf\n",sumshifts,nshifts,((double) sumshifts)/nshifts); */
    }else{
	//relevant section
	ll_node* hd = initialize_ll(argv[1], &n);
	ll_node* tl = hd->prev;
	hd->prev=NULL;

	if(argc >= 3 && !strcmp(argv[2],"-b")){
	    luka_ll(hd,tl,n,write_ll);
	}else{
	    luka_ll(hd,tl,n,print_ll);
	}
    }

    return 0;
}
