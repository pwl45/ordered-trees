
# Fixed-Content Lukasiewicz Words

### Compilation: 

On a unix-like system, you should be able to compile everything by typing `make`

### Execution
`luka` is given a list of frequencies as its first argument. Running
`./luka 3,1,1,1`
will generate and output all Lukasiewicz words with 3 zeroes, 1 one, 1 two, and 1 three.  Similarly, 
`./luka 6,1,3,0,1`
generates and outputs all Lukasiewicz words with 6 zeroes, 1 one, 3 twos, 0 threes, and 1 four.

The frequencies given to `luka` should translate to a multiset with a sum equal to its length.
For example, 3,1,1,1 -> {0,0,0,1,2,3} which has sum 6 and length 6.

The program colors each "increase" in the string by default (relevant to the ordering described by the paper).  This can be turned off by adding the flag -n to the end of the command (so, for example, `./luka 3,1,1,1 -n` outputs the same Lukasiewicz words as the first command, but without any colored numbers. 

Finally, the -v flag adds some arrows to visualize the shifts that are used to iterate between strings.  So 
`./luka 3,1,1,1 -v`
would generate the same strings as the first command but with arrows illustrating the left-shifts.

Running ./luka -h displays a small help menu with most of this information.



