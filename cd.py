#!/usr/bin/env python3
import sys

def print_dyck(a):
    print(a[1:])

# todo
def simple_motzkin(s,t,visit):
    a = [-1] + [2] * s + [1] * t + [0] * s
    n = 2 * s + t
    m = n

    last_two = s
    last_one = s+t
    #last_zero is always m
    
    while(True):
        if m == n:
            a[2] = 0
            a[last_two+1] = 2
            last_two+=1
            a[last_one+1] = 1
            last_one+=1



def cool_dyck(s,visit):
    a = [-1] + [1] * s + [0] * s
    # a = [-1] + [1]*s + [0]*s  # 1-based indexing
    n = 2*s
    m = n
    
    last_one = s

    # print(len(a),m,last_one,a[last_one],a[last_one+1])
    while(True):
        if m == n:
            a[2] = 0
            a[last_one+1] = 1
            m=2
            last_one = 1
        elif a[m + 2]  == 1:
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
                a[last_one+1] = 1
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
        visit(a)
        if m == n:
            break

    





if __name__ == '__main__':
    cool_dyck(int(sys.argv[1]),print_dyck)
