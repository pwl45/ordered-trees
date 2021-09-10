#!/usr/bin/env python3
import sys
from termcolors import *
increase_colors = ["bright_red_ul", "green", "blue", "yellow", "magenta", "cyan"]

def multiset_from_frequencies(freqs):
    freqdict = {}
    for i in range(0, len(freqs)):
        freqdict[i] = freqs[i]
    # print(freqdict)
    ms = []
    for key in freqdict:
        ms += [int(key)] * int(freqdict[key])
    return ms

def fixed_growth(ms):
    # This could be changed to zero if the first partition should be one
    maxval=-1
    for m in ms:
        # print(maxval)
        diff = m-maxval
        if diff > 1:
            return False
        else:
            maxval = max(maxval,m)
    return True

def append_ms(ms, results):
    results.append(ms.copy())

def right_shift(ms, index):
    if index == 0:
        shift_index = 0
    elif ms[index-1] > ms[index + 1]:
        shift_index = index
    else:
        shift_index = index-1
    ms.insert(len(ms), ms.pop(shift_index))

    return shift_index

def cool_fixed_filter(ms,visit):
    # print('here')
    # get the list into non-decreasing order first
    ms.sort()
    results = []

    # ITERATION ONE: 
    # we start in non-decreasing order, so we know the whole multiset is non-decreasing. 
    # so we use the left pointing triangle function on ms[len(ms)-1]
    first_inc = 0
    last_shift = right_shift(ms,first_inc)

    while(True):
        if ms[len(ms)-2] > ms[len(ms)-1]:
            first_inc = len(ms)-2
        elif first_inc == 0:
            visit(ms,results)
            return results
        else:
            first_inc-=1

        if fixed_growth(ms):
            visit(ms,results)

        last_shift = right_shift(ms,first_inc)

def lex_cool(ms,visit):
    ms.sort()
    results = []
    n = len(ms)-1
    first_dec = 0
    last_shift = right_shift(ms,first_dec)

    while(True):
        if ms[n] > ms[n-1]:
            first_dec = n-1 
        elif last_shift == 0:
            if first_dec == 0:
                if fixed_growth(ms):
                        visit(ms,results)
                return results
            else:
                first_dec-=1
        else:
            first_dec-=1
        if fixed_growth(ms):
            visit(ms,results)

        last_shift = right_shift(ms, first_dec)

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

def find_right_shift(pre, post):
    pairs = []
    if len(pre) != len(post):
        return False
    for i in range(0, len(pre)):
        for j in range(i+1, len(pre)):
            precp = pre.copy()
            precp.insert(j,precp.pop(i))
            if precp == post:
                pairs.append((i,j))
    if len(pairs) == 0:
        print("Something went wrong: No shift gray code between consecutive permutations")
        pretty_print_ms(pre)
        pretty_print_ms(post)
        exit(1)
    return pairs

def pretty_print_ms_rightincs(ms,color=True):
    result = "["
    found = 0
    value_colors = [-1] * len(ms)
    decs = []
    for i in range(1, len(ms)):
        index = len(ms)-1-i
        if ms[index] > ms[index+1]:
            value_colors[index] = found
            decs.append(index)
            found +=1
        
    
    for i in range(0, len(ms)):
        index = len(ms)-1-i
        if i != 0:
            result += ", "
        if value_colors[i] >= 0:
            # incs.append(i)
            if color:
                if value_colors[i] < len(increase_colors):
                    color = increase_colors[value_colors[i]]
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
    return decs

def print_debug_right(permutations, color):
        # stuff for printing the strings
        decs = []
        for i in range(0, len(permutations)):
            perm = permutations[i]
            prevperm = permutations[i-1]
            if i > 0:
                candidate_shifts = find_right_shift(prevperm,perm)
                arrow_indices = candidate_shifts[len(candidate_shifts)-1]
                arrow_string=""
                for j in range(0, arrow_indices[1] * 3):
                    if j < arrow_indices[0] * 3 + 1:
                        arrow_string += " "
                    elif j == arrow_indices[0] * 3 + 1:
                        arrow_string += "|"
                    # elif j == arrow_indices[1] * 3: 
                    #     arrow_string += ">"
                    else:
                        arrow_string += "-"
                arrow_string += ">|"
                print(arrow_string)
                ind_diff = arrow_indices[0]-decs[0]
                dest_diff = len(perm)-1 - arrow_indices[1]
                # if ind_diff != -1 and ind_diff != 0:
                #     print("unexpected: difference between shifted index and first (from the right) decrease wasn't -0 or -1")
                #     print("pre and post:")
                #     print(prevperm)
                #     print(perm)
                #     # print(ind_diff)
                #     exit(0)
                
                # print("SHIFTED VAL AND DISTANCE FROM END:",prevperm[arrow_indices[0]],dest_diff)
                # if dest_diff != prevperm[arrow_indices[0]]:
                #     print("unexpected: ms[i] wasn't shifted to index len(ms)-1-ms[i]")
                #     print("pre and post:")
                #     print(prevperm)
                #     print(perm)
                #     exit(0)

                preval = prevperm[decs[0]-1]
                postval = prevperm[decs[0]+1]
                if ind_diff == 0:
                    print("i",end="\t")
                    red = True
                else:
                    print("i-1",end="\t")
                    red = False

                if preval <= postval:
                    print("LE",end="\t")
                    le = True
                else:
                    print("G",end="\t")
                    le = False
            
                print()
                # if postval <= preval and ind_diff != -1:
                #     looseness = len(prevperm[decs[0]:]) - sum(prevperm[decs[0]:])
                #     if looseness > prevperm[decs[0]-1]:
                #         print("This should never happen")
                #         exit(0)
                    # print(len(prevperm[decs[0]:]))
                    # print(sum(prevperm[decs[0]:]))



                # if postval > preval and ind_diff != 0:
                #     print("This should never happen")
                #     exit(0)

                print()
            decs = pretty_print_ms_rightincs(perm, color)


if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print_usage()
    else:
        freqs=sys.argv[1].split(',')
        ms = multiset_from_frequencies(freqs)
        permutations=cool_fixed_filter(ms,append_ms)

        print("\npermutations:")
        print_debug_right(permutations, True)
        # for perm in permutations:
        #     print(perm)


