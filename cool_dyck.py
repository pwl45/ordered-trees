#!/usr/bin/env python3
import sys

def left_shift_motzkin(ms,insert_index, shift_index, prefix_len,last_prefix_occurrences):
    ms[insert_index] = ms[shift_index]
    if shift_index == prefix_len + 1:
        ms[prefix_len+1] = ms[prefix_len]

    for i in range(0,3):
        index = last_prefix_occurrences[i] 
        if index >= insert_index and index < shift_index:
            ms[index+1] = i

def print_onebased(a,x,y):
    print(a[1:])
def print_zerobased(a,x,y):
    print(a[:-1])


def getxyz(b):
    x = 0
    y = 0
    z = 0
    for i in range(1,len(b)):
        if i > 1 and b[i] > b[i-1]:
            x=i
            break
        elif b[i] == 2:
            z = i+1
        elif b[i] == 1:
            y = i+1
    if z == 0:
        z = 1
        # pass
    if y == 0:
        y = z
    if x == 0:
        x = len(b)
    # if x == 0:
    #     x = y
    # print("")
    # print("in getxyz")
    # print(b)
    # print(z,y,x)
    # print("")
    return (x,y,z)

# uncomment the return here and you get some debug output
def printv(*args):
    return
    print(*args)
def coolMotzkin(t, s, visitFn):
    n = 2*s + t
    # safe to assume s >= 1???
    # if string is all ones, that'll break this because b[y] will give index out of bounds
    b = [-1] + [2]*s + [1]*t + [0]*s  # 1-based indexing
    x = s+t # very temporary: should be first increase but there is none
    y = s+t+1 # first 0 (actually first past 1's)
    z = s+1 # first 1 (actually first past 2's)
            
    # visitFn(b,x,y)
    printv(b[1:])
    while x <= n:  # 1's can be in the last position, but not 2's ... ?
        q = b[x-1]
        r = b[x]  # Will we need to remember b[x] before overwriting it?
        # really would like something better than this
        if x < n:
            r1 = b[x+1]
        else:
            r1 = r
        printv("z:",z,"y:",y,"x:",x,"\nq:",q,"r:",r,"r1:",r1)
        b[x] = b[x-1] # try equals 0?
        b[y] = b[y-1] # try equals 1?
        b[z] = b[z-1] # try equals 2?
        b[1] = r
        # printv(b)
        y += 1
        z += 1
        x += 1
        # Does the above make sense for initial instructions?
        # Garbage below.
        # don't think we need to check x<n here, but if something breaks putting that back could fix it
        # q < r1:
        #     note q can only be 0 or 1
        #     r1 can be 1 or 2
        #     r1 == 0 implies q >= r1
        #     after handling r1==0, if r1 is not zero, we know that if it's the le case, r1=1,q-1,r=2. we shift 1
        #     if it's the g case, r1=1 is the special case
        #     SO, IF r1==1

        if q < r1:
            # merge with case where it's tight
            # this means that the first increase is 1
            # so there must have been a zero preceding it
            # No prefix can start with all ones and zeroes (like a close without an open)
            # so we know that there's a two at the front if r is 1, and thus we create an increase by shifting
            if r == 1: # could be and b[2] == 2
                y = 2
                x = 2
                z = 1
            printv("G")
            pass
        else:
            printv("LE")
            # BIG NOTE: The LE case (b[x+1] <= b[x-1] always means creating an increase at the front
            # (with the exception of the =0 and tight case)
            # This is because we're shiftin i+1.  and x+1 is less than or equal to x-1.  and x > x-1.  so x > x+1. 
            # thus, x+1 cannot be two because nothing is bigger than two. 


            # z-2: number of zeroes; x-y: number of ones (both have beein incremented; cancels out)
            # printv("test vars:",z,y,x,q,r,s)

            if r1 == 0:
                if z-2 > (x-y):
                    # printv("shift b[x+1]=0")
                    # position two minus r?
                    b[1] = 2
                    b[2] = 0
                    # b[r1-1] = 
                    # really first_increase+1
                    b[x] = r
                    z=2
                    y=2
                    x=3
                else:
                    x+=1
            else:
                # we're shifting index i+1
                printv(r,r1)

                # TODO: maybe merge this with q < r1 case
                # to do this: we know q isn't 2.  so q - r1 is at most 1
                b[x] = r
                b[x-1] = q
                b[1] = r1
                z = 1
                if b[2] == 2:
                    y = 2
                    x = 2



        # printv("")
        visitFn(b,x,y)    
        # (t,u,v) = getxyz(b)
        # if (t,u,v) != (x,y,z):
        #     printv(t,u,v)
        #     printv(x,y,z)
        #     input()
        # (x,y,z) = (t,u,v)
def motz_wrapper(t,s,visitFn):
    # print("here")
    ms = [2]*s + [1]*t + [0]*(s+1)  # 1-based indexing
    prefix_motzkin(ms,visitFn)

def prefix_motzkin(ms, visit):
    # print("prefix motza")
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    new_prefix_len=prefix_len
    prefix_sum=prefix_len-1
    if ms[0] == 1 or len(ms) == 3:
        visit(ms,results,results)
        return results

    #can be simplified for (s,t) input type
    last_prefix_occurrences = [-1,-1,-1]
    for i in range(0,prefix_len):
        last_prefix_occurrences[ms[i]] = i

    # TODO: keep track of number of 2s and number of zeroes in prefix instead of sum
    while(True):
        is_tight = prefix_len == prefix_sum
        # CASE 0:
        insert_index = 0
        if prefix_len == len(ms):
            insert_index=1
            shift_index=len(ms)-1
        # CASE 1: ms[i+1] > ms[i-1]
        elif ms[prefix_len+1] > ms[prefix_len-1]:
            shift_index = prefix_len
            new_prefix_len = prefix_len+1
        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1 (ms[i+1] != 0) and CASE 2.2.1 (ms[i+1] == 0 and not tight)
            if prefix_sum > prefix_len or ms[prefix_len+1] > 0:
                shift_index = prefix_len+1
                if ms[shift_index] == 0:
                    insert_index = 1
                new_prefix_len = prefix_len+1
            # CASE 2.2.2: ms[i+1] == 0 and tight
            else:
                shift_index = prefix_len
                if prefix_len == len(ms) - 3:
                    new_prefix_len = len(ms)
                else:
                    new_prefix_len = prefix_len+2

        left_shift_motzkin(ms,insert_index, shift_index,prefix_len,last_prefix_occurrences)

        shift_val = ms[insert_index]
        if shift_val == 0:
            prefix_sum = 2
            prefix_len = 2
            # could also set each individually, not sure if this creates a new list in a bad way
            last_prefix_occurrences = [1,-1,0]
        elif shift_val == 1 and ms[1] == 2:
            prefix_sum = 1
            prefix_len = 1
            last_prefix_occurrences = [-1,0,-1]
        else: 
            for i in range(3):
                if last_prefix_occurrences[i] >= 0:
                    last_prefix_occurrences[i]+=1
                elif i == ms[insert_index]:
                    last_prefix_occurrences[i] = insert_index
            # WEIRD CASE: when you shift a 2 to the front instead of a zero because the list is tight,
            # the last zero is now further along
            # there's now a new zero at the end of the string
            if new_prefix_len==prefix_len + 2:
                last_prefix_occurrences[0] = prefix_len+1
            prefix_len = new_prefix_len
            prefix_sum += ms[insert_index]

        visit(ms,results,results)

        if(prefix_len == len(ms)):
            return results


def coolDyck(t, visitFn):
    n = 2*t
    b = [-1] + [1]*t + [0]*t  # 1-based indexing
    x = t
    y = t
    visitFn(b)
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
        visitFn(b)
    

def cool_dyck(s,visit):
    a = [-1] + [1] + [0] + [1] * (s-1) + [0] * (s-1)
    n = 2*s
    m = 2
    
    last_one = 1

    # print(len(a),m,last_one,a[last_one],a[last_one+1])
    while(m != n):
        visit(a)
        if a[m + 2]  == 1:
            # shift a[m+1]
            a[m+1] = 0
            a[last_one+1] = 1
            last_one += 1
            m += 1
        else:
            # shift a[m+2] if we can, otherwise do a[m+1]
            # we "can" when 2*last_one > m
            if 2*last_one > m:
                # we can shift a[m+2]
                a[2] = 0
                a[m] = 1
                a[m+1] = 0
                a[m+2] = 1
                m=2
                last_one = 1
            else:
                # we can't shift a[m+2]: settle for m+1 instead
                a[m+1] = 0
                a[last_one+1] = 1
                last_one += 1
                m += 2




if __name__ == '__main__':
    if len( sys.argv ) < 2:
        exit(1)
    else:
        gen=coolMotzkin
        visit=print_onebased
        s=-1
        t=-1

        # dumb but functional way of handling arguments 
        for i in range(1, len(sys.argv)):
            arg = sys.argv[i]
            diff_mode = False
            if arg[0] == '-':
                for i in range(1,len(arg)):
                    argchar = arg[i]
                    if argchar == 'h':
                        exit(0)
                    elif argchar == 'r':
                        gen=motz_wrapper
                        visit=print_zerobased
                    elif argchar == 's':
                        gen=coolMotzkin
                        visit=print_onebased
            else:
                if t == -1:
                    t=int(sys.argv[i])
                elif s == -1:
                    s=int(sys.argv[i])
    print(t,s)
    gen(t,s,visit)

