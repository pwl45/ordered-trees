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

void swap(int* a, int* b){
    //this is fun
    *a ^= *b;
    *b ^= *a;
    *a ^= *b;
    //should probably be changed before publishing, though
}

//this is more fun than it should be
void rev(int* lo, int n){
    for(int* hi = lo + n - 1; hi > lo; swap((hi--),(lo++)));
}


int* generate_ms(char* frequencies, int* nptr, int* maxptr){

    const char delim[2] = ",";

    char* token = strtok(frequencies, delim);

    int sz = 1;
    int* ms = malloc(sizeof(int)*sz);
    int n=0;

    int i = 0;
    int max = 0;
    while(token){

	/* printf("%d: %d\n",i,atoi(token)); */
	// this assignmment is necesary because realloc can change where ms starts
	int freq = atoi(token);
	if(freq){
	    ms = append_ms(ms, &n, &sz, i,freq);
	    max=freq;
	}
	i++;
	token = strtok(NULL, delim);
    }
    ms = realloc(ms,n*sizeof(int));

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

void luka(int* ms, int n, void (*visit)(int* ms, int n)){
    int prefix_len,prefix_sum,shift_index,insert_index;
    int* incs = (int*) malloc(sizeof(int)*max(ms,n));
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
		    /* incs[--nincs-1]--; */
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
		stack_push(incs,&nincs,insert_index+1);
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
    int *ms = generate_ms(argv[1],&n, &max);
    rev(ms,n);
    luka(ms,n,print_ms);

    return 0;
}
