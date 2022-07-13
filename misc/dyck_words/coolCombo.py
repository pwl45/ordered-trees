import sys
from coolCommon import visitPrint

# Cool-lex order of (s,t)-combinations (i.e., binary srings with s 0s and t 1s)
# using prefix left-shifts (i.e., a bit is moved into the first position).
# Moreover, each shift can be accomplished using at most two transposition, or
# equivalently, at most four assignments.
#
# It is a loopless algorithm that stores the combination in an array.
# More accurately, it uses a Python list in a way that is equivalent to an array,
# and it uses 1-based indexing, which is somewhat common in academic settings.
# (Python lists use 0-based indexing, so we add a 'dummy' value -1 at index 0.)
#
# During each iteration, but the first, the two index variables do the following:
#  - y is the first index with b[y] = 0.
#  - x is the first index with b[x-1] = 0 and b[x] = 1.
#    In other words, it is the index of the first increase.
#
# The general strategy of each iteration is as follows.
# It optimistically assumes that the array will have a prefix of the form
#
#    1* 0+ 1 1
#
# where * means zero or more, and + means one or more.  In other words, we
# optimistically assume that non-increasing prefix is followed by at least two 1s.
# When this is the case, it is relatively easy to create the next string.
# More specifically, the first four instructions,
#
#     b[x] = 0, b[y] = 1, x += 1, y += 1
#
# are sufficient.  For example, below is a sample prefix of this type, and the
# result, with x and y updated.  [NOTE: My editor uses 4-space tabs.]
#
#     111100011   becomes   111110001
#         y  x                   y  x
#
# The rest of the code handles situations where our optimistic assumption is not
# true.  One case actually requires no attention.  Specifically, if the entire
# string is just 1* 0+ 1 (i.e., there is no second symbol after the non-increasing
# prefix), then the above work is sufficient.  More generally, the first four
# in each loop handle the cases where the symbol following the non-increasing
# prefix is shifted, rather the second symbol following the non-increasing
# prefix.  The remaining case occurs when we have a prefix of the following
#
#    1* 0+ 1 0
#
# In this case, the second symbol after the non-increasing prefix should have
# been shifted.  However, the work that we've already done is not incorrect.
# Instead, we just need to do more work.  Specifically, we must set the first
# bit to 0.  We may also need to update x and y.  The update of x and y is
# required when the 1* is non-empty.  (It that prefix 1* is empty, then the
# string starts with 0, so moving a 0 into the first position does not create
# a new leftmost increase 01; if the prefix 1* is non-empty, then we will
# have created a new increase 01 at the front of the string, and we need to
# update x and y accordingly.)
#
# The final trick involves the first iteration.  When the string is entirely
# non-increasing, (i.e. it has the form 1^t 0^s), then x would be undefined.
# So it doesn't make sense to initialize x to anything.  Instead, we initialize
# x and y so that the first two instructions in the while loop don't do anything.
# Namely, we initialize x = t and y = t, and then the while loop begins by
# setting b[x] = b[t] = 0 and b[y] = b[t] = 1, which effectively does nothing
# other than changing b[t] from 1 to 0, and then back from 0 to 1.  After the next
# two instructions, x += 1 and y += 1, we have the y is set to the correct value.
# For example, after the first four instructions in the while loop, the initial
# string will be modified as follows.
#
#     11110000   becomes   11110000
#        x                     x
#        y                     y
#
# In other words, nothing has changed, except that y is now properly set (while
# x remains incorrect since it would be undefined still).  The code in the if
# statement manages to finish the correct modification, as shown below.
#
#     11110000   becomes   11110000   becomes   01111000
#        x                     x                yx
#        y                     y
#
# So the first iteration is tricky.  The remaining iterations all follow the
# pattern discussed above.
#
# The algorithm ends when x is incremented past the end of the array.
#
# Note: This impelmentation visits the non-increasing string first.  When viewing
# cool-lex order recursively, it makes more sense for this to be visited last.

def coolCombo(t, s, visitFn):
    n = s+t
    b = [-1] + [1]*t + [0]*s  # note: 1-based indexing
    x = t  # note: tricky values for the first iteration
    y = t
    visitFn(b,x,y)
    while x < n:
        b[x] = 0 # the order of these two is important on first loop
        b[y] = 1
        x += 1
        y += 1
        if b[x] == 0:
            b[x] = 1
            b[1] = 0
            if b[2] == 1:  # note: this test is not needed for Dyck words
                x = 2
                y = 1
        visitFn(b,x,y)

if __name__ == "__main__":
    t = int(sys.argv[1])
    s = int(sys.argv[2])
    coolCombo(t, s, visitPrint)
