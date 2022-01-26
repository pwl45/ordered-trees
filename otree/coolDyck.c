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
    putchar(b[n]+48);
    putchar('\n');
    /* printf("\n"); */
}

//s zeroes, t ones
int rankDyck(uint8_t* b, int s, int t){
    int n = s+t;
    printdyck(b,n);
    printf("%d %d\n",s,t);

    //still one based indexing
    if(b[n]==0){
	printf("Trailing zero\n");
	printf("\n");
	return rankDyck(b,s-1,t);
    }else{
	//we know b[n] == 1
	int currInd = n-1;
	while(b[currInd] == 0){
	    //1^{t-1}0^s1
	    currInd--;
	}
	if(currInd == t-1){
	    printf("Cardinal string\n");
	    printf("K(%d,%d)-1\n",t,s);
	    printf("\n");
	    return 0;
	}
	else{
	    printf("Not cardinal string\n");
	    printf("K(%d,%d)\n",t-1,s);
	    printf("\n");

	    //leftover is t-1 ones and s-((n-1)-(currInd)) zeroes
	    return 0 + rankDyck(b,s-(n-1-currInd),t-1);
	}
    }
    printf("Should never reach here\n");
    return 0;
}

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

//convenience
uint8_t* strToDyck(char* dword){
    int n = strlen(dword);
    uint8_t* b = (uint8_t*) malloc(sizeof(uint8_t)*(n+1));
    b[0] = -1;
    for(int i = 1; i < n+1; i++){
	printf("%d: %c\n",i,dword[i-1]);
	b[i] = dword[i-1]-48;

	printf("%d\n",b[i]);
    }

    return b;
}

int main(int argc, char** argv){
    /* char* dword = "101100"; */
    
    /* printf("%s\n",dword); */
    /* int n = strlen(dword); */
    /* uint8_t* b = strToDyck(dword); */

    /* rankDyck(b,3,3); */
    /* printdyck(b,n); */

    if(argc < 2)
	exit(1);
    coolDyck(atoi(argv[1]));
}
