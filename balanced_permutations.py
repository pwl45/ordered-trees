#!/usr/bin/env python3
import sys
from termcolors import *
from datetime import datetime,timedelta
increase_colors = ["bright_red_ul", "green", "blue", "yellow", "magenta", "cyan"]

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

def append_ms(ms, results):
    results.append(ms.copy())

def cool_balanced_stack(ms, visit):
    ms.sort(reverse=True)
    results = []
    incs = []
    ms.insert(1, ms.pop(len(ms)-1))
    # after this, we know that the first increase is at index 2 if it exists
    prefix_sum = ms[0]
    if ms[1] < ms[2]:
        incs.append(2)
    insert_index = 1
    visit(ms,results)
    while(True):
        if len(incs) == 0:
            return results
        first_inc = incs.pop()
        is_tight = first_inc == prefix_sum

        # CASE 1: ms[i+1] > ms[i-1]
        if ms[first_inc+1] > ms[first_inc-1]:
            # first check if we're removing an increase by shifting this left
            if ms[first_inc+1] > ms[first_inc]:
                incs.pop()
            # We create an increase by shifting here: push first_inc+1 to stack
            incs.append(first_inc+1)

            shift_index = first_inc
            # we know the number being shifted is positive since it's the first inc
            insert_index = 0

        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1 (ms[i+1] != 0) and CASE 2.2.1 (ms[i+1] == 0 and not tight)
            if not is_tight or ms[first_inc+1] > 0:
                # Check if we removed an increase 
                if first_inc < len(ms) - 2 and ms[first_inc+2] > ms[first_inc+1] and ms[first_inc+2] <= ms[first_inc]:
                    incs.pop()
                shift_index = first_inc+1

                if ms[shift_index] > 0:
                    insert_index = 0
                else:
                    insert_index = 1

                # We move the previous first_inc further down the list here: push first_inc+1
                incs.append(first_inc+1)

            # CASE 2.2.2: ms[i+1] == 0 and tight
            else:
                # We don't create an increase by shifting here
                if ms[first_inc+1] > ms[i]:
                    incs.pop()
                shift_index = first_inc
                # we're shifting first inc, so it goes to the front
                insert_index = 0

        ms.insert(insert_index, ms.pop(shift_index))
        # In every case we want to check if we just created an inc at the front
        # except for if we inserted 
        if ms[insert_index] < ms[insert_index+1]:
            prefix_sum = ms[0]
            # We already checked for an increase at first_inc; don't double count
            if insert_index != first_inc:
                incs.append(insert_index+1)
        else:
            prefix_sum += ms[insert_index]
        visit(ms,results)
            
            
def cool_balanced(ms,visit):
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

    while(True):
        # print(ms)
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
            visit(ms,results)
            return results
        elif not need_scan:
            # Add the most recently inserted value to the prefix sum
            prefix_sum += ms[insert_index]
            first_inc+=1
        else:
            prefix_sum += ms[insert_index]
            for i in range(first_inc+1,len(ms)):
                if ms[i] > ms[i-1]:
                    first_inc = i
                    break
            else:
                visit(ms,results)
                return results

        # if balanced(ms):
        # print(ms)
        visit(ms,results)
        # print_ms(ms)

        # # not necessary for now
        # prefix_sum_reference=calc_prefix_sum(ms)
        # if prefix_sum != prefix_sum_reference:
        #     print("bad: prefix sum is being calculated wrong")
        #     exit(1)

        # print(prefix_sum,first_inc)
        (shift_index, insert_index,need_scan) = balanced_left_shift(ms,first_inc,prefix_sum==first_inc)

def cool_balanced_filter(ms,visit):

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

def print_ms_visit(ms,results):
    # print("here")
    print(ms)

def pretty_print_ms_visit(ms,results):
    pretty_print_ms(ms)

# needs to be refactored: 
# make getting the list of incs separate from printing the list
def pretty_print_ms(ms,color=True):
    result = "["
    found = 0
    incs = []
    for i in range(0, len(ms)):
        if i != 0:
            result += ", "
        if i > 0 and ms[i] > ms[i-1]:
            incs.append(i)
            if color:
                if found < len(increase_colors):
                    color = increase_colors[found]
                else:
                    color="red"
                result += color_string(str(ms[i]),color)
                found += 1
            else:
                result += str(ms[i])
        else:
            result += str(ms[i])

    result += "]"
    print(result)
    incs.reverse() 
    return incs

def print_usage():
    usage_string ='''Usage: ./balanced_permutations.py [options] frequencies
Frequencies is a list of comma separated frequencies with no spaces

Options:
-s: (s)tack mode
Utilizes a stack to attain loopless generation of balanced multiset permutations
Without this flag, generation is technically not loopless. 

-f: (f)ilter mode
Generates all permutations of the multiset and filters to only output the balanced ones. 
Default behavior generates the balanced permutations directly without filtering
-g: (d)ebu(g) mode
Shows a visualization of the shift, tells whether it was the ith or i+1st element that was shifted, and whether or not the i+1st element was zero 


-p: (p)rint-only mode
prints the multisets without storing them in memory
Disables debug mode since debug mode requires looking back at the previous permutation to visualize the shifts
Necessary for processing large multisets without using up unreasonable amounts of ram

-q: (q)uiet-mode
not especially useful, but fast

-n: (n)o-color mode
Prints multisets without coloring the first increase
Useful for outputting results to files as most text editors will not render terminal escape sequences as colors

-d: diff mode
Doesn't output time results or whether or not the permutations are being generated via filter
Useful for testing with diffs so that diffs between -f and not -f can be nothing if correct

-l latex mode
Outputs permutations as \otree{[permutation]} to facilitate use with latex
Works well with -d flag to get the \otree{...} output without anything else before or after

-h: help
Prints this help menu and exits'''
    print(usage_string)
    return


# really should be refactored, but it works
# should also make it not print colors if color=False
def print_debug(permutations, color):
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
            incs = pretty_print_ms(perm, color)
            if len(incs) > 0:
                red_index = incs.pop()
            else:
                red_index = len(ms)-1

def print_perms(permutations,color):
    # print(permutations)
    if color:
        for perm in permutations:
            pretty_print_ms(perm,color)
        return
    else:
        for perm in permutations:
            print(perm)

# color parameter is not used, but there for compatibility
def print_otrees(permutations,color):
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
        generate_perms=cool_balanced
        filter = False
        verbose = False
        debug = False
        color = True
        print_only = False
        quiet=False
        visit = append_ms
        output = print_perms
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
                        output=print_debug
                    elif argchar == 'f':
                        generate_perms=cool_balanced_filter
                    elif argchar == 'n':
                        color=False
                    elif argchar == 'p':
                        print_only = True
                    elif argchar == 'q':
                        quiet = True
                    elif argchar == 's':
                        generate_perms=cool_balanced_stack
                    elif argchar == 'd':
                        diff_mode = True
                    elif argchar == 'l':
                        output=print_otrees
                    else:
                        print("Invalid argument: -", argchar,sep="")
                        print("Run ./balanced_permutations.py -h to see a list of options and their behaviors.")
                        exit(1)
            else:
                freqs=arg.split(',')

        if print_only:
            if color:
                visit=pretty_print_ms_visit
            else:
                visit=print_ms_visit

        start_time = datetime.now()
        ms = multiset_from_frequencies(freqs)
        if not diff_mode:
            # Sum must be equal to len-1
            print("SUM:",sum(ms), "LEN:",len(ms))
        if sum(ms) != len(ms) - 1:
            exit(1)

        if not diff_mode:
            print("Initial multiset:",ms)
            print("Generating using",generate_perms.__name__)

        permutations = generate_perms(ms,visit)

        end_time = datetime.now()
        time_to_generate = end_time-start_time
        # print(end_time)
        # delta = timedelta(start_time,end_time)
        # print(delta)
        if visit == append_ms and not quiet:
            output(permutations,color)

        post_print = datetime.now()
        print_time = post_print - end_time
        total_time = post_print - start_time
        if not diff_mode:
            print("Time spent generating:",formatted_timedelta(time_to_generate))
            if visit == append_ms and not quiet:
                print("Time spent printing:",formatted_timedelta(print_time))
                print("Permutations generated:",len(permutations))
                # print("Permutations per second, excluding prints:",len(permutations))
            print("Total time:",formatted_timedelta(total_time))

