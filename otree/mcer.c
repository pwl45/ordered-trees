#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
uint8_t* b;
int n;

/* long int calls=0; */
/* long int generated=0; */

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


//This function basically just sets 
//b=(10)^n
//dumb way of doing this, M.C. Er
void GenerateOrderedTrees(int x, int y){
  /* calls++; */

  if(!x && !y){
    printdyck(b,2*n);
    /* generated++; */
    return;
  }
  if(y){
    b[2*n-(2*x + y)+1] = 0;
    /* printf("heay\n"); */
    GenerateOrderedTrees(x,y-1);
  }
  if(x){
    b[2*n-(2*x+y)+1]=1;
    /* printf("hoy\n"); */
    GenerateOrderedTrees(x-1,y+1);
  }
}

int main(int argc, char *argv[])
{
  n = atoi(argv[1]);
  b = (uint8_t*) calloc(sizeof(uint8_t),(2*n+1));
  GenerateOrderedTrees(n,0);
  /* printf("%ld,%ld, %lf\n",generated,calls,((double)calls)/generated); */
  return 0;
}
