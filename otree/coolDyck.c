#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

void printdyck(uint8_t* b, int n){

    /* return; */

    for(int i = 0; i < n-1; i++){
	putchar(b[i+1]+48);
	/* putchar(','); */
	/* printf("%c,",(b[i+1]+48)); */
    }
    putchar(b[n+1]+48);
    putchar('\n');
    /* printf("\n"); */
}

/* void rankDyck(uint8_t* b, int s, int t){ */
/*     int n = s+t; */
/*     if(b[){ */
/*     }else{ */
/*     } */
/* } */

//slightly modified version of coolDyck that starts with 10111...000... and ends with 1111...0000...
void coolDyck(int t){
    int n = 2*t;

    // one based indexing; uses calloc so we only need to set the ones 
    uint8_t* b = (uint8_t*) calloc(sizeof(uint8_t),(n+1));
    b[0]=-1;

    //INITIAL STRING: 101111...0000....
    b[1]=1;
    b[2]=0;
    memset(b+3,1,t-1);
    memset(b+3+t-1,0,t-1);

    int x=3;
    int y=2;

    printdyck(b,n);
    while (x <= n) {
	b[x]=0;
	b[y]=1;
	x++;
	y++;
	if(b[x] == 0){
	    if(x >= 2*y-2){
		x++;
	    }else{
		//shift 0
		b[x]=1;
		b[2]=0;
		x=3;
		y=2;
	    }
	}
	printdyck(b,n);
    }
}

int main(int argc, char** argv){
    if(argc < 2)
	exit(1);
    coolDyck(atoi(argv[1]));
}
