# https://oeis.org/A055151

from __future__ import print_function  # Python 2/3 compatibility.
import sys  # For command-line arguments sys.argv.

def isLuka(string):
    sum = 0
    for value in string:
        sum += value-1
        if sum < 0:
            return False
    return True

# This function is called every time a new permutations is created.
def visit(perm):
    print(*perm, sep=" ")

# Create the next multiset permutation in cool-lex order.
#  - perm is the current multiset permutation.
#  - inc is the smallest index with perm[inc] < perm[inc].
#    This index exists if and only if perm is not last in cool-lex order.
# Returns the new inc index.
def update(perm, inc):
    # Pop the value at index inc+1 or inc+2 and push it to the front.
    index = inc+1 if inc == len(perm)-2 or perm[inc] < perm[inc+2] else inc+2
    value = perm.pop(index)
    perm.insert(0, value)

    # Return the updated inc index.
    return 0 if perm[0] < perm[1] else inc+1

# Generates the cool-lex order of any multiset of symbols.
#  - multiset is a list of pairwise comparable values.
def coollex(multiset):
    # Initialize n to be the number of symbols in the multiset.
    # Initialize perm to the last permutation in cool-lex order.
    # Initialize inc to n-2.
    L = []
    n = len(multiset)
    perm = sorted(multiset, reverse = True)
    inc = n-2

    # Repeatedly update and visit the next permutation in cool-lex order.
    # Note: inc is undefined for the last permutation in cool-lex order.
    #       inc = n-2, n-1 are used as special cases to start and end of the loop.
    while inc != n-1:
        inc = update(perm, inc)
        L.append(list(perm))

    return L

for n in range(2,11):
    for s in range(0,int(n/2)+1):
    #for s in range(int(n/2),-1,-1):
        multiset = s*[2] + (n-2*s)*[1] + s*[0]
        assert(len(multiset) == n)

        # Run the cool-lex algorithm .
        # Reduce or filter the list to Lukasiewicz words!
        L1 = coollex(multiset)
        L1 = [string for string in L1 if isLuka(string)]
        print(len(L1), end=" ")

print("")
#
