# Ordered Trees

### Compilation: 

On a unix-like system, you should be able to compile everything by typing `make`

### Execution

To generate all ordered trees with n non-root nodes (i.e., n+1 nodes), run `./otree n`

By default, each generated tree has its corresponding Dyck word printed.  To instead generate LaTex code to see a visual representation of the ordered trees, run `./otree n -o`.  This output can be copy-pasted into a LaTex document that uses the packages tikz and tikz-qtree.

Alternatively, a wrapper script `./optikz.sh` is provided that adds the necessary header/footer to the output of `./otree n -o` and compiles the resulting LaTex document automatically.  Running `./optikz.sh n -o` outputs the C_n ordered trees with n+1 nodes to the file `texput.pdf`.  

As an example, the output of `./optikz 5 -o` is stored in `sampletrees.pdf`.

### Other Files

There are many other, less relevant files in here. 

`otree-standalone.c` is a simplified version of otree where all relevant code is in one file. 

`otree-noparent.c` demonstrates that

`mcer.c` implements the algorithm from M.C. Er's "Enumerating Ordered Trees Lexicographically" (1985). 

Files inside of `array-implementation` provide an alternate implementation in which each ordered tree stores an array of children (instead of a linked list).

