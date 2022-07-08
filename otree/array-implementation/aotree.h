struct arraynode {
    int nch; //not  strictly necessary
    int maxch;
    struct arraynode* parent;
    struct arraynode** children;
};

typedef struct arraynode anode;

void print_atree_as_dyck(anode* n);
anode* new_anode(int maxch);
anode* get_initial_atree(int t);
