#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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

//term branchless is used liberally
void branchless_luka(int* ms, int n, void (*visit)(int* ms, int n)){
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
	// branchlessness comes at a cost... 3 multiplications sucks
	prefix_sum = prefix_sum*!incfront + ms[0]*incfront;
	prefix_sum += ms[insert_index]*!incfront;


	visit(ms,n);
    }
}

void luka(int* ms, int n, void (*visit)(int* ms, int n)){
    int prefix_len,prefix_sum,shift_index,insert_index;
    int* incs = (int*) malloc(sizeof(int)*(n/2));
    int nincs = 1;
    incs[0]=n;
    while(nincs){
	prefix_len = incs[nincs-1]++; //greedy increase of the first increase
	if(prefix_len >= n-1){
	    nincs--;
	    shift_index = n-1;
	    insert_index = !(ms[n-1]); //nice bang
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

int main(int argc, char *argv[])
{
    if(argc < 2){
	printf("usage: ./luka frequencies\n");
	exit(1);
    }

    int n;
    int max;
    int *ms = initialize_ms(argv[1],&n, &max);
    rev(ms,n);
    ms[n]=666; //if we see 666 anywhere in the multiset, we've shifted from out of bounds.
    luka(ms,n,print_ms);

    return 0;
}
