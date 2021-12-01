# Generate the permutations of any multiset in "cool-lex order".
# Cool-lex order is a Gray code in which one symbol moves to the front of the permutation to create the next.
# A. Williams "Loopless Generation of Multiset Permutations using a Constant Number of Variables by Prefix Shifts" (SODA 2009)
# https://www.researchgate.net/publication/220779544_Loopless_Generation_of_Multiset_Permutations_using_a_Constant_Number_of_Variables_by_Prefix_Shifts

from __future__ import print_function  # Python 2/3 compatibility.
import sys  # For command-line arguments sys.argv.

def isNecklace(A, smallest=True):
    if smallest == True:
        for i in range(1,len(A)):
            if (A[i:]+A[:i]) < A:
                return False
        return True
    else:
        for i in range(1,len(A)):
            if (A[i:]+A[:i]) > A:
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

# Read the multiset as a command-line argument.
# And create a negative version which will switch incs to decs.
multiset = [int(arg) for arg in sys.argv[1:]]
multisetNeg = [-value for value in multiset]

# Run the cool-lex algorithm on normal and negative version.
L1 = coollex(multiset)
L2 = coollex(multisetNeg)

# Flip the negative back to positive.
L2 = [[-value for value in string] for string in L2]

# Reduce the lists to necklaces!
L1 = [string for string in L1 if isNecklace(string)]
L2 = [string for string in L2 if isNecklace(string)]

# Print out the normal.
print("Cool to first non-decreasing section")
for string in L1:
    print(*string, sep="")
print("")

# Print out the negative version.
print("Cool to first non-increasing section")
for string in L2:
    print(*string, sep="")
print("")

# Print out the normal, but co'ed it.
print("Cool to last non-decreasing section")
for string in L1:
    print(*(reversed(string)), sep="")
print("")

# Print out the negative version, but flip it back to positive, and co'ed it.
print("Cool to last non-increasing section")
for string in L2:
    print(*(reversed(string)), sep="")
print("")


