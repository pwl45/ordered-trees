#include "luka.h"

ll_node* new_llnode(int data, ll_node* prev, ll_node* next){
    ll_node* node = (ll_node*) malloc(sizeof(ll_node*));
    node->data=data;
    node->prev=prev;
    node->next=next;
    return node;
}

void print_ll(ll_node* hd){
    /* printf("["); */
    if(hd){
        printf("%d",hd->data);
    }
    while( (hd=hd->next) ){
    /* while( (hd=hd->next)->next ){ */
        printf("%d",hd->data);
    }
    /* printf("]"); */
    printf("\n");
}

ll_node* appendluka(int i, ll_node* tl){
    ll_node* newtl = new_llnode(i, tl, NULL);
    tl->next = newtl;
    return newtl;
}

ll_node* getluka_rec(ll_node* hd, ll_node* tl, node* n){
    if(!n){
        return NULL;
    }
    int i = 0;
    node* curr = n->left_child;
    while(curr){
        curr=curr->right_sibling;
        i++;
    }
    /* printf("%d\n",i); */

    if(hd == NULL && tl == NULL){
        hd = new_llnode(i,NULL,NULL);
        tl = hd;
    }else{
        tl = appendluka(i,tl);
    }

    curr = n->left_child;
    while(curr){
        tl = getluka_rec(hd,tl, curr);
        curr=curr->right_sibling;
    }

    return tl;
}

ll_node* getluka(node* n){
    ll_node* tl = getluka_rec(NULL,NULL,n);
    ll_node* hd = tl;
    /* printf("here\n"); */
    for(; hd->prev; hd = hd->prev);

    /* printf("here\n"); */

    /* tl->prev->next=NULL; */

    return hd;
    /* print_ll(hd,-1); */
}
