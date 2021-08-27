#!/usr/bin/env python3
import sys
from termcolors import *
from datetime import datetime,timedelta

def balanced(ms):
    sum = 0
    for i in range(0, len(ms) - 1):
        sum += ms[i]
        if sum < i+1:
            # print(ms, sum,i)
            return False
    return ms[len(ms)-1] == 0

def calc_prefix_sum(ms):
    sum = ms[0]
    for i in range(1, len(ms)):
        if ms[i] <= ms[i-1]:
            prefix_sum_reference=calc_prefix_sum(ms)
            sum += ms[i]
        else:
            break
    return sum

def is_shift(pre, post):
    pairs = []
    if len(pre) != len(post):
        return False
    for i in range(0, len(pre)):
        for j in range(i+1, len(pre)):
            precp = pre.copy()
            precp.insert(i,precp.pop(j))
            if precp == post:
                pairs.append((i,j))
    if len(pairs) == 0:
        print("Something went wrong: No shift gray code between consecutive permutations")
        exit(1)
    return pairs

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


def balanced_left_shift(ms,first_inc,is_tight):
    need_scan = False
    if first_inc == len(ms)-1:
        shift_index = len(ms)-1
    elif ms[first_inc+1] > ms[first_inc-1]:
        shift_index = first_inc
    else:
        # we "want" to do first_inc+1
        # but only if we can
        # and we can't if it's zero and the non-inc prefix of the list is tight
        if not is_tight or ms[first_inc+1] > 0:
            shift_index = first_inc+1
        else:
            need_scan = True
            shift_index = first_inc
    # for now, calling the index at which we insert the shifted value insert_index
    if ms[shift_index] > 0:
        insert_index = 0
    else:
        insert_index = 1

    ms.insert(insert_index, ms.pop(shift_index))

    # Return the index that was left shifted since that seems like a useful thing to know
    return (shift_index, insert_index, need_scan)
            
            
def cool_balanced(ms):
    ms.sort(reverse=True)
    results = []

    # ITERATION ONE: 
    # we start in non-decreasing order, so we know the whole multiset is non-decreasing. 
    # so we use the left pointing triangle function on ms[len(ms)-1]
    # list is sorted, so we know that the first shift will be shifting a zero at the end of the list to index 1
    ms.insert(1, ms.pop(len(ms)-1))
    # after this, we know that the first increase is at index 2 if it exists
    prefix_sum = ms[0]
    if ms[1] < ms[2]:
        first_inc = 2
    else:
        # This actually means we're done - the list is all zeroes except for the first value. 
        # Could just return here, but it's handled elswhere for now
        first_inc = len(ms) -1 
    insert_index = 1
    need_scan = False

    while(True):
        # print_ms(ms,True)
        if ms[insert_index] < ms[insert_index+1]:
            # if a non-zero value is inserted, it will always be inserted at index zero
            # being inside the if means that there is an increase between 0 and 1,
            # thus making the prefix sum just ms[0]
            # conveniently, if a zero is inserted, it will always be inserted at index 1
            # this guarantees that the non-increasing prefix is the first value and then some number of zeroes
            # since any positive number following a zero is an increase
            # so the sum of the non-inc prefix will also just be ms[0]
            prefix_sum = ms[0]
            first_inc = insert_index+1 
        elif first_inc == len(ms)-1:
            results.append(ms.copy())
            return results
        elif not need_scan:
            # Add the most recently inserted value to the prefix sum
            prefix_sum += ms[insert_index]
            first_inc+=1
        else:
            # print("NEED SCAN")
            prefix_sum += ms[insert_index]
            for i in range(first_inc+1,len(ms)):
                if ms[i] > ms[i-1]:
                    # print("Length of scan: ",i-first_inc)
                    first_inc = i
                    break
            else:
                # print(ms)
                results.append(ms.copy())
                return results

        # if balanced(ms):
        # print(ms)
        results.append(ms.copy())
        # print_ms(ms)

        # # not necessary for now
        # prefix_sum_reference=calc_prefix_sum(ms)
        # if prefix_sum != prefix_sum_reference:
        #     print("bad: prefix sum is being calculated wrong")
        #     exit(1)

        # print(prefix_sum,first_inc)
        (shift_index, insert_index,need_scan) = balanced_left_shift(ms,first_inc,prefix_sum==first_inc)

# having this as a separate function is probably unnecessary and bad for maintenance
def cool_balanced_print(ms):
    ms.sort(reverse=True)
    results = []

    # ITERATION ONE: 
    # we start in non-decreasing order, so we know the whole multiset is non-decreasing. 
    # so we use the left pointing triangle function on ms[len(ms)-1]
    # list is sorted, so we know that the first shift will be shifting a zero at the end of the list to index 1
    ms.insert(1, ms.pop(len(ms)-1))
    # after this, we know that the first increase is at index 2 if it exists
    prefix_sum = ms[0]
    if ms[1] < ms[2]:
        first_inc = 2
    else:
        # This actually means we're done - the list is all zeroes except for the first value. 
        # Could just return here, but it's handled elswhere for now
        first_inc = len(ms) -1 
    insert_index = 1
    need_scan = False

    while(True):
        # print_ms(ms,True)
        if ms[insert_index] < ms[insert_index+1]:
            # if a non-zero value is inserted, it will always be inserted at index zero
            # being inside the if means that there is an increase between 0 and 1,
            # thus making the prefix sum just ms[0]
            # conveniently, if a zero is inserted, it will always be inserted at index 1
            # this guarantees that the non-increasing prefix is the first value and then some number of zeroes
            # since any positive number following a zero is an increase
            # which will have
            prefix_sum = ms[0]
            first_inc = insert_index+1 
        elif first_inc == len(ms)-1:
            print(ms)
            # results.append(ms.copy())
            return results
        elif not need_scan:
            # Add the most recently inserted value to the prefix sum
            prefix_sum += ms[insert_index]
            first_inc+=1
        else:
            # print("NEED SCAN")
            prefix_sum += ms[insert_index]
            for i in range(first_inc+1,len(ms)):
                if ms[i] > ms[i-1]:
                    # print("Length of scan: ",i-first_inc)
                    first_inc = i
                    break
            else:
                print(ms)
                # results.append(ms.copy())
                return results

        # if balanced(ms):
        print(ms)
        # results.append(ms.copy())
        # print_ms(ms)

        # # not necessary for now
        # prefix_sum_reference=calc_prefix_sum(ms)
        # if prefix_sum != prefix_sum_reference:
        #     print("bad: prefix sum is being calculated wrong")
        #     exit(1)

        # this return value isn't currently used, but it may be useful later so keeping it for now
        # print(prefix_sum,first_inc)
        (shift_index, insert_index,need_scan) = balanced_left_shift(ms,first_inc,prefix_sum==first_inc)

def cool_lex_print(ms):

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
            print(ms)
            return
            # results.append(ms.copy())
            # return results
        else:
            first_inc+=1

        if balanced(ms):
            print(ms)
            # results.append(ms.copy())

        # this return value isn't currently used, but it may be useful later so keeping it for now
        last_shift = left_shift(ms, first_inc)

def cool_lex(ms):

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
            results.append(ms.copy())
            return results
        else:
            first_inc+=1

        if balanced(ms):
            results.append(ms.copy())
        # results.append(ms.copy())

        # this return value isn't currently used, but it may be useful later so keeping it for now
        last_shift = left_shift(ms, first_inc)

def multiset_from_frequencies(freqdict):
    ms = []
    for key in freqdict:
        ms += [int(key)] * int(freqdict[key])
    return ms

# TODO: This really shouldn't be responsible for finding the first increasing value

def str_ms(ms, color=True):
    result = "["
    found = 0
    returnval = 0
    for i in range(0, len(ms)):
        if i != 0:
            result += ", "
        if i > 0 and found < 2 and ms[i] > ms[i-1]:
            # result += str(ms[i])
            if found == 0:
                if color:
                    result += TERM_RED(str(ms[i]))
                else:
                    result += str(ms[i])
                returnval = i
            elif found == 1:
                # result += TERM_GREEN(str(ms[i]))
                result += str(ms[i])
            found += 1
        else:
            result += str(ms[i])

    result += "]"
    return result

def print_ms(ms,color=True):
    result = "["
    found = 0
    returnval = 0
    for i in range(0, len(ms)):
        if i != 0:
            result += ", "
        if i > 0 and found < 2 and ms[i] > ms[i-1]:
            # result += str(ms[i])
            if found == 0:
                if color:
                    result += TERM_RED(str(ms[i]))
                else:
                    result += str(ms[i])
                returnval = i
            elif found == 1:
                # result += TERM_GREEN(str(ms[i]))
                result += str(ms[i])
            found += 1
        else:
            result += str(ms[i])

    result += "]"
    print(result)
    return returnval

def print_usage():
    usage_string ='''Usage: ./balanced_permutations.py [options] frequencies
Frequencies is a list of comma separated frequencies with no spaces

Options:
-g: (d)ebu(g) mode
shows a visualization of the shift, tells whether it was the ith or i+1st element that was shifted, and whether or not the i+1st element was zero 

-f: (f)ilter mode
generates all permutations of the multiset and filters to only output the balanced ones. 
Normal behavior generates the balanced permutations directly without filtering

-p: (p)rint-only mode
prints the multisets without storing them in memory
disables debug mode since debug mode requires looking back at the previous permutation to visualize the shifts
necessary for processing large multisets without using up unreasonable amounts of ram

-q: (q)uiet-mode
not especially useful, but fast

-n: (n)o-color mode
prints multisets without coloring the first increase
useful for outputting results to files as most text editors will not render terminal escape sequences as colors

-d: diff mode
Doesn't output time results or whether or not the permutations are being generated via filter
Useful for testing with diffs so that diffs between -f and not -f can be nothing if correct

-h: help
prints this help menu and exits'''
    print(usage_string)
    return

def print_details(permutations, color):
        # stuff for printing the strings
        for i in range(0, len(permutations)):
            perm = permutations[i]
            if i > 0:
                candidate_shifts = is_shift(permutations[i-1],perm)
                arrow_indices = candidate_shifts[0]
                arrow_string=""
                for j in range(0, arrow_indices[1] * 3 + 1):
                    if j < arrow_indices[0] * 3 + 1:
                        arrow_string += " "
                    elif j == arrow_indices[0] * 3 + 1:
                        arrow_string += "|"
                    elif j == arrow_indices[0] * 3 + 2: 
                        arrow_string += "<"
                    else:
                        arrow_string += "-"
                arrow_string += "|"
                print(arrow_string)
                ind_diff = red_index-candidate_shifts[0][1]
                preval = permutations[i-1][red_index-1]
                postval = permutations[i-1][red_index+1]
                if ind_diff == 0:
                    print("i",end="\t")
                    red = True
                else:
                    print("i+1",end="\t")
                    red = False

                if postval <= preval:
                    print("LE",end="\t")
                    le = True
                else:
                    print("G",end="\t")
                    le = False

                if postval == 0:
                    print("Z")
                    z = True
                else:
                    print("NZ")
                    z = False
                
                if le == False and red == False:
                    print("This should never occur")
                    exit(0)

                print()
            red_index=print_ms(perm, color)

def print_simple(permutations,color):
    if color:
        for perm in permutations:
            print_ms(perm,color)
        return
    else:
        for perm in permutations:
            print(perm)

def print_otrees(permutations):
    for perm in permutations:
        print("\\otree{" + str(perm[0]),end="")
        for val in perm[1:]:
            print(", " + str(val),end="")
        print("}")

def formatted_timedelta(delta):
    delta_str = str(delta)
    index = 0
    for i in range(0, len(delta_str)):
        if delta_str[i] != '0' and delta_str[i] != ':':
            index = i
            break

    return delta_str[index:]



if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print_usage()
    else:
        filter = False
        verbose = False
        debug = False
        color = True
        print_only = False
        quiet = False
        latex_mode = False
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
                    elif argchar == 'g':
                        debug=True
                    elif argchar == 'f':
                        filter = True
                    elif argchar == 'n':
                        color=False
                    elif argchar == 'p':
                        print_only = True
                        debug = False
                        quiet = True
                    elif argchar == 'q':
                        quiet = True
                    elif argchar == 'd':
                        diff_mode = True
                    elif argchar == 'l':
                        latex_mode = True
                        diff_mode = False
                        debuge=False
                        print_only=False
                    else:
                        print("Invalid argument: -", argchar,sep="")
                        exit(1)
            else:
                freqs=arg.split(',')

        # ms as shorthand for multiset
        start_time = datetime.now()
        freqdict = {}
        for i in range(0, len(freqs)):
            freqdict[i] = freqs[i]
        ms = multiset_from_frequencies(freqdict)
        if not diff_mode and not latex_mode:
            print(freqdict)
            # Sum must be equal to len-1
            print("SUM:",sum(ms), "LEN:",len(ms))
        if sum(ms) != len(ms) - 1:
            exit(1)

        if filter:
            if not diff_mode:
                print("generating all and filtering")
            if print_only:
                permutations = cool_lex_print(ms)
            else:
                permutations = cool_lex(ms)
        else:
            if not diff_mode and not latex_mode:
                print("doing balanced directly")
            if print_only:
                permutations = cool_balanced_print(ms)
            else:
                permutations = cool_balanced(ms)
        end_time = datetime.now()
        gen_diff = end_time-start_time
        # print(end_time)
        # delta = timedelta(start_time,end_time)
        # print(delta)
        if debug:
            print_details(permutations,color)
        elif latex_mode:
            print_otrees(permutations)
        elif not quiet:
            print_simple(permutations,color)
        post_print_time = datetime.now()
        print_diff = post_print_time - end_time
        total_diff = post_print_time - start_time
        if not diff_mode and not latex_mode:
            print("Time spent generating:",formatted_timedelta(gen_diff))
            if not print_only:
                print("Time spent printing:",formatted_timedelta(print_diff))
                print("Permutations generated:",len(permutations))
                # print("Permutations per second, excluding prints:",len(permutations))
            print("Total time:",formatted_timedelta(total_diff))

