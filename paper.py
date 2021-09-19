#!/usr/bin/env python3
import sys
increase_colors = ["bright_red_ul", "green", "blue", "yellow", "magenta", "cyan"]

def is_balanced(ms):
    sum = 0
    for i in range(0, len(ms) - 1):
        sum += ms[i]
        if sum < i+1:
            # print(ms, sum,i)
            return False
    return ms[len(ms)-1] == 0


def right_shift(ms, index):
    if index == 0:
        shift_index = 0
    elif ms[index+1] > ms[index - 1]:
        shift_index = index
    else:
        shift_index = index-1
    ms.insert(len(ms), ms.pop(shift_index))

    return shift_index


def suffix_filter(ms,visit):
    ms.sort(reverse=True)
    results = []
    n = len(ms)-1
    first_dec = 0
    last_shift = right_shift(ms,first_dec)

    while(True):
        if ms[n] > ms[n-1]:
            first_dec = n-1 
        elif last_shift == 0:
            if first_dec == 0:
                visit(ms,results)
                return results
            else:
                first_dec-=1
        else:
            first_dec-=1
        if balanced(ms):
            visit(ms,results)

        last_shift = right_shift(ms, first_dec)

def is_suffix_tight(ms,first_dec,suffix_sum):
    suffix_len = len(ms)-1-first_dec
    total_sum = suffix_sum + ms[first_dec] + ms[first_dec-1] + 1
    # print("len:",suffix_len,end='\t')
    # print("sum:",suffix_sum)
    return suffix_len+2 == total_sum
 
def right_shift_index(ms,shift_index):
    shift_val = ms.pop(shift_index)
    insert_index = len(ms)-shift_val
    ms.insert(insert_index,shift_val)
    return (shift_val,insert_index)

def suffix_direct(ms,visit):
    ms.sort(reverse=True)
    results = []
    decs = []
    # shift_val,insert_index=right_shift_index(ms,0)

    # if insert_index > 0 and ms[insert_index-1] < ms[insert_index]:
    #     decs.append(insert_index-1)
    # suffix_sum = shift_val
    # visit(ms, results)
    first_dec = 0
    suffix_sum = len(ms) - 1
    while(True):
        # print(ms)
        # print(decs)
        # print()
        if first_dec == 0:
            shift_index = first_dec
        # CASE 1: ms[i+1] > ms[i-1]
        # shift i 
        elif ms[first_dec+1] > ms[first_dec-1]:
            # first check if we're removing a decrease by shifting this right
            if ms[first_dec-1] < ms[first_dec]:
                decs.pop() 
            decs.append(first_dec-1)
            shift_index = first_dec
            # calculate insert index at the end
        
        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1: ms[i] != 0 and CASE 2.2.1 (ms[i] == 0 and not tight)
            # shift i - 1
            if not is_suffix_tight(ms,first_dec,suffix_sum) or ms[first_dec] > 0:
                # Check if we removed an increase
                if first_dec > 1 and ms[first_dec-2] < ms[first_dec-1] and ms[first_dec-2] >= ms[first_dec]:
                    decs.pop() 
                shift_index = first_dec-1
                # calculate insert index at the end
                decs.append(first_dec-1)

            # CASE 2.2.1 ms[i] == 0 and tight
            # shift i 
            else:
                # We don't create an increase by shifting here
                shift_index = first_dec
                suffix_sum += ms[first_dec-1]
        shift_val,insert_index = right_shift_index(ms,shift_index)

        if shift_val > 0 and insert_index > 0:
            if shift_val > ms[insert_index-1]:
                decs.append(insert_index-1)
                suffix_sum = shift_val
            else:
                suffix_sum += shift_val
        # else:
        #     # if we shift a zero, it must be the first decrease (index i)
        #     # because we only shift i-1 when ms[i+1] <= ms[i-1]; we know ms[i-1] > 0 since ms[i] was a decrease
        #     # the decrease is maintained
        #     pass
        #     # this seems almost too good to be true

        visit(ms, results)
        if len(decs) == 0:
            return results
        else:
            first_dec = decs.pop()

            

    return results

def left_shift(ms, index):
    if index >= len(ms)-1:
        shift_index = len(ms)-1
    elif ms[index-1] < ms[index + 1]:
        shift_index = index
    else:
        shift_index = index+1
    ms.insert(0, ms.pop(shift_index))

    # Return the index that was left shifted since that seems like a useful thing to know
    return shift_index

def prefix_direct(ms, visit):
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    prefix_sum=prefix_len-1
    incs=[]
    if ms[0] == 1:
        visit(ms,results)
        return results
    while(True):
        is_tight = prefix_len == prefix_sum
        # CASE 0:
        if prefix_len == len(ms):
            insert_index=1
            shift_index=len(ms)-1
        # CASE 1: ms[i+1] > ms[i-1]
        elif ms[prefix_len+1] > ms[prefix_len-1]:
            # first check if we're removing an increase by shifting this left
            if ms[prefix_len+1] > ms[prefix_len]:
                incs.pop()
            # We create an increase by shifting here: push prefix_len+1 to stack
            incs.append(prefix_len+1)

            shift_index = prefix_len
            # we know the number being shifted is positive since it's the first inc
            insert_index = 0

        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1 (ms[i+1] != 0) and CASE 2.2.1 (ms[i+1] == 0 and not tight)
            if prefix_sum > prefix_len or ms[prefix_len+1] > 0:
                # Check if we removed an increase 
                if ms[prefix_len+2] > ms[prefix_len+1] and ms[prefix_len+2] <= ms[prefix_len]:
                    incs.pop()
                shift_index = prefix_len+1

                if ms[shift_index] > 0:
                    insert_index = 0
                else:
                    insert_index = 1

                # We move the previous prefix_len further down the list here: push prefix_len+1
                incs.append(prefix_len+1)

            # CASE 2.2.2: ms[i+1] == 0 and tight
            else:
                # We don't create an increase by shifting here

                # this can't happen: ms[prefix_len+1] is zero, can't be greater than anything
                # if ms[prefix_len+1] > ms[prefix_len]:
                #     incs.pop()
                shift_index = prefix_len
                # we're shifting first inc, so it goes to the front
                insert_index = 0

        ms.insert(insert_index, ms.pop(shift_index))
        # In every case we want to check if we just created an inc at the front
        # except for if we inserted 
        if ms[insert_index] < ms[insert_index+1]:
            prefix_sum = ms[0]
            # We already checked for an increase at prefix_len; don't double count
            if insert_index != prefix_len:
                incs.append(insert_index+1)
        else:
            prefix_sum += ms[insert_index]
        visit(ms,results)
        if(len(incs) == 0):
            return results
        else:
            prefix_len=incs.pop()

def prefix_filter(ms,visit):

    # get the list into non-decreasing order first
    ms.sort(reverse=True)
    results = []

    # ITERATION ONE: 
    # we start in non-decreasing order, so we know the whole multiset is non-decreasing. 
    # so we use the left pointing triangle function on ms[len(ms)-1]
    first_inc = len(ms)-1
    last_shift = left_shift(ms,first_inc)

    while(True):
        if ms[0] < ms[1]:
            first_inc = 1
        elif first_inc == len(ms)-1:
            visit(ms,results)
            return results
        else:
            first_inc+=1

        if balanced(ms):
            visit(ms,results)

        # this return value isn't currently used, but it may be useful later so keeping it for now
        last_shift = left_shift(ms, first_inc)

def multiset_from_frequencies(freqs):
    freqdict = {}
    for i in range(0, len(freqs)):
        freqdict[i] = freqs[i]
    # print(freqdict)
    ms = []
    for key in freqdict:
        ms += [int(key)] * int(freqdict[key])
    return ms

def print_ms_visit(ms,results):
    print(ms)

def print_usage():
    usage_string ='''Usage: ./balanced_permutations.py [options] frequencies
Frequencies is a list of comma separated frequencies with no spaces

Options:
-l: (l)eft shifts
Generates balanced permutation looplessly using left shifts. Default behavior.

-r: (r)ight shifts
Generates balanced permutation looplessly using right shifts

-f: (f)ilter mode
Generates all permutations of the multiset and filters to only print balanced permuations.
Default behavior generates the balanced permutations directly without filtering

-h: help
Prints this help menu and exits'''
    print(usage_string)
    return

if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print_usage()
    else:
        generate_perms=prefix_direct
        quiet=False
        visit = print_ms_visit
        dir = 'l'
        filter = False
        # output = print_perms
        # you can now do something like -gfn instead of -g -f -n
        # this would mean debug output, generate permutations via filter, and print with no color
        for i in range(1, len(sys.argv)):
            arg = sys.argv[i]
            diff_mode = False
            if arg[0] == '-':
                for i in range(1,len(arg)):
                    argchar = arg[i]
                    if argchar == 'h':
                        print_usage()
                        exit(0)
                    elif argchar == 'f':
                        filter = True
                    elif argchar == 'l':
                        dir = 'l'
                    elif argchar == 'r':
                        dir = 'r'
                    else:
                        print("Invalid argument: -", argchar,sep="")
                        print("Run ./balanced_permutations.py -h to see a list of options and their behaviors.")
                        exit(1)
            else:
                freqs=arg.split(',')

            if dir == 'l': 
                generate_perms = prefix_filter if filter else prefix_direct
            elif dir == 'r': 
                generate_perms = suffix_filter if filter else suffix_direct
            else:
                print("error: invalid direction")

        ms = multiset_from_frequencies(freqs)
        print("SUM:",sum(ms), "LEN:",len(ms))
        if sum(ms) != len(ms) - 1:
            exit(1)

        print("Initial multiset:",ms)
        # print("Generating using",generate_perms.__name__)

        generate_perms(ms,visit)

