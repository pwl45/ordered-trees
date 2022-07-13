#!/usr/bin/env python3
import sys
# print("top of file")
# from coolCommon import visitPrint

# Generates Dyck words.
# See the comments in coolCombo.py.
#
# The main difference is that the following test:
#
#
#     if x >= 2*y - 2:
#
# This checks the following: Is it valid to swap the two symbols after the
# non-increasing prefix.  In other words, is it value to shift the 0 or not?
# Note that x and y have been incremented at this point already.  So the test
# works out as follows.  Let #1s be the number of 1s in the non-increasing prefix
# at the start of the loop, and let #0s' denote the number of 0s in the
# non-increasing prefix after the proposed swap (i.e., it is #0s+1).  Then the
# can be understood as follows:
#
#   #0s' > #1s   (if this is true, then the swap is invalid)
#   (x-y)+1 > y-2
#   x > 2*y - 3
#   x >= 2*y - 2
#
# Note that x == 2*y - 2 could also be used.  In other words, we can replace the
# inequality test with an equality test, without any change of function.
#
# For example, the test will succeed for strings with prefixes like the following:
#
#     1111000010
#
# since after the swap (i.e., the start of shifting the 0), we'd end up with the
# following prefix
#
#     1111000001
#
# which is invalid.  Note that the above test logic is equivalent to checking if
# the non-increasing prefix tight (i.e, #0s = #1s).  However, this is not the
# best way of viewing the test, since a tight test does not work for (1/k)-ary
# Dyck words (see coolkCatalan.py).
#
# When the test succeeds, it's actually good news for the program, since the
# optimistic shift is the correct shift.  In other words, if we have a prefix
# like 1111000010, then the 1 should be shifted, which is what the initial four
# instructions have already done.  All that is left to do is update x.  At first
# it may seem like we need to scan for the next 1, or store the values in a stack,
# but we don't need to do this.  For example, if 1111000010 is a prefix, then we
# know that the very next symbol must be 1.  So we can just x += 1 for the update.
#
# The remaining case, where the 0 is actually shifted, is handled similarly to
# the (s,t)-combinations case, but there are some differences since the 0 is
# shifted into the second position, rather than the first position, and we know
# that a new leftmost increase is created (why?).

def visitPrint(b,g,d):
    print(b[1:])

def coolDyck(t, visitFn):
    n = 2*t
    b = [-1] + [1]*t + [0]*t  # 1-based indexing
    x = t
    y = t
    visitFn(b,x,y)
    while x < n-1:
        b[x] = 0 # this is equivalent to b[x] = b[x-1] (setest e coolMotzkin.py)
        b[y] = 1
        x += 1
        y += 1
        if b[x] == 0:
            if x >= 2*y - 2: # test (see comments above function)
                x += 1   # we know that B[x+1] == 1 because Dyck word
            else:
                b[x] = 1
                b[2] = 0 # note the difference from coolCombo's b[1] = 0
                x = 3 # note the difference from coolCombo's x = 2
                y = 2 # note the difference from coolCombo's y = 1
        visitFn(b,x,y)

if __name__ == "__main__":
    # print("here!")
    t = int(sys.argv[1])
    # print(t)
    coolDyck(t, visitPrint)
