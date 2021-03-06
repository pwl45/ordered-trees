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


def find_left_shift(pre, post):
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
        pretty_print_ms(pre)
        pretty_print_ms(post)
        exit(1)
    return pairs

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
 
def ref_suf_sum(ms):
    i=len(ms)-1
    total=0
    while i>=0:
        if i == len(ms)-1:
            total += ms[i]
        else:
            if ms[i] < ms[i+1]:
                return total
            else:
                total += ms[i]
        i -= 1
    return total

def right_shift_index(ms,shift_index):
    shift_val = ms.pop(shift_index)
    insert_index = len(ms)-shift_val
    ms.insert(insert_index,shift_val)
    return (shift_val,insert_index)

def pd_concise(ms, visit):
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    prefix_sum=prefix_len-1
    incs=[]
    if ms[0] == 1:
        visit(ms,results)
        return results
    while(True):
        print(ms)
        print(prefix_len)
        is_tight = prefix_len == prefix_sum
        # CASE 0:
        if prefix_len == len(ms):
            insert_index=1
            shift_index=len(ms)-1
        elif ms[prefix_len+1] == 0:
            if prefix_sum > prefix_len:
                shift_index = prefix_len+1
                insert_index = 1
                # We move the previous prefix_len further down the list here: push prefix_len+1
                incs.append(prefix_len+1)
            else:
                if ms[prefix_len+2] > ms[prefix_len+1] and ms[prefix_len+2] <= ms[prefix_len]:
                    incs.pop()
                shift_index = prefix_len
                # we're shifting first inc, so it goes to the front
                insert_index = 0
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
            # Check if we removed an increase 
            if ms[prefix_len+2] > ms[prefix_len+1] and ms[prefix_len+2] <= ms[prefix_len]:
                incs.pop()
            shift_index = prefix_len+1

            insert_index = 0
            # We move the previous prefix_len further down the list here: push prefix_len+1
            incs.append(prefix_len+1)

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

def cool_dyck(ms,visit):
    ms.sort(reverse=True)
    results = []
    prefix_len = len(ms)
    # can be simplified for s,t case
    last_prefix_occurrences = [-1,-1-1]
    for i in range(0,len(ms)):
        print(ms[i])
        print(len(last_prefix_occurrences))
        last_prefix_occurrences[ms[i]] = i
    while(True):
        visit(ms,results)
        if prefix_len == len(ms):
            print(last_prefix_occurrences[2])
            ms[last_prefix_occurrences[2] + 1] = 2
            ms[1] = 2

        if prefix_len == len(ms):
            return results

def left_shift_motzkin(ms,insert_index, shift_index, prefix_len,last_prefix_occurrences):
    ms[insert_index] = ms[shift_index]
    if shift_index == prefix_len + 1:
        ms[prefix_len+1] = ms[prefix_len]

    for i in range(0,3):
        index = last_prefix_occurrences[i] 
        if index >= insert_index and index < shift_index:
            ms[index+1] = i

def prefix_motzkin(ms, visit):
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    new_prefix_len=prefix_len
    prefix_sum=prefix_len-1
    if ms[0] == 1 or len(ms) == 3:
        visit(ms,results)
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

        visit(ms,results)

        if(prefix_len == len(ms)):
            return results

def suffix_direct(ms,visit):
    ms.sort(reverse=True)
    results = []
    decs = []

    first_dec = 0
    suffix_sum = len(ms) - 1
    while(True):
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

def maxheight(ms):
    curr=0
    maxh=0
    for m in ms:
        curr += m-1
        maxh=max(curr,maxh)
    return maxh
    
#multi digit numbers do not exist as far as this function is concerned
def basic_tostr(ms):
    res=""
    for m in ms:
        res += str(m)


    return res

#multi digit numbers do not exist as far as this function is concerned
def colored_tostr(ms,prefix_len,shift_index):
    res=""
    res+="\\underline{"
    # prefix_len = min(prefix_len,len(ms)-1)
    added=False
    for i in range(len(ms)):
        if i == shift_index:
            res+="\\color{deeppurple}\\textbf{" + str(ms[prefix_len]) + "}\\color{black}"
        else:
            res+=str(ms[i])
        if i == prefix_len-1 or i == len(ms)-1 and not added:
            res+="}"
            added=True

    # for i in range(min(prefix_len,len(ms))):
    #     res+=str(ms[i])

    # res += "}"
    
    # if prefix_len < len(ms):
    #     res+="\\color{deeppurple}\\textbf{" + str(ms[prefix_len]) + "}\\color{black}"

    # for i in range(prefix_len+1,len(ms)):
    #     res+=str(ms[i])


    return res
# 4a -> n_2
# 4b -> m1_1
# 4c -> m2_1
# 4d -> m2_2
def LukaTable(ms):
    result="\\LukaTable["+str(maxheight(ms))+"]{" + str(ms[0])
    for val in ms[1:]:
        result+="," + str(val)
    result+="}"
    return result

def lukatex(ms,results,prefix_len,shift_index,insert_index):
    # print(ms)
    lukatable=LukaTable(ms)
    if prefix_len >= len(ms):
        case="n_2"
    elif insert_index==1: # shifting a zero
        case="m2_2"
    elif shift_index == prefix_len:
        case="m1_1"
    elif shift_index == prefix_len+1:
        case="m2_1"
    else:
        print("bad: no case")
        exit(1)

    # todo: change if you drop the zero at the end
    print(lukatable,end=" & ")

    # print(basic_tostr(ms),end=" & ")
    print(colored_tostr(ms,prefix_len,shift_index),end=" & ")

    # prefix_len could be len(ms)+1 because of the extra zero
    print(min(prefix_len,len(ms)),end=" & ")
    print("\\eqref{eq:prefix_",case,"}",sep="",end=" & ")
    print("$\\leftshift{",shift_index+1,"}{",insert_index+1,"}$",sep="",end=" & ")
    scut_ind=get_scut_ind(ms)
    if scut_ind == -1:
        scut="\\epsilon"
    else:
        scut=basic_tostr(ms[scut_ind:])
    print("$",scut,"$",sep="",end=" ") # scut
    print("\\\\")
    

#4a: shifting the last thing (read: zero): should always be shift_index=len(ms)-2 and insert_index=1
#4b: shifting something e
#TODO: this doesn't need its own function at all, need to refactor
def prefix_lukatex(ms, visit):
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    prefix_sum=prefix_len-1
    incs=[]
    if ms[0] == 1:
        # visit(ms,results)
        return results
    while(True):
        is_tight = prefix_len == prefix_sum
        # CASE 0:
        # >= len(ms)-1 means it's either the last thing in the prefix zero or the last real zero. 
        if prefix_len >= len(ms)-1:
            shift_index=len(ms)-1
            if ms[shift_index] == 0:
                insert_index=1
            else:
                insert_index=0
        # CASE 1: ms[i+1] > ms[i-1]
        elif ms[prefix_len+1] > ms[prefix_len-1]:
            # first check if we're removing an increase by shifting this left
            if ms[prefix_len+1] > ms[prefix_len]:
                incs.pop()
            # We create an increase by shifting here: push prefix_len+1 to stack
            incs.append(prefix_len+1)

            shift_index = prefix_len
            # we know the number being shifted is positive since it's the first inc
            # insert to the head
            insert_index = 0

        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1 (ms[i+1] != 0) and CASE 2.2.1 (ms[i+1] == 0 and not tight)
            if prefix_sum > prefix_len or ms[prefix_len+1] > 0:
                # Check if we removed an increase 
                if prefix_len < len(ms)-2 and ms[prefix_len+2] > ms[prefix_len+1] and ms[prefix_len+2] <= ms[prefix_len]:
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

        lukatex(ms[:-1],results,prefix_len,shift_index,insert_index)
        # print(prefix_len,shift_index,insert_index)
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

        if(len(incs) == 0):
            prefix_len=len(ms)
            return results
        else:
            prefix_len=incs.pop()

def prefix_general(ms, visit):
    ms.sort(reverse=True)
    results = []
    prefix_len=len(ms)
    prefix_sum=prefix_len-1
    incs=[]
    if ms[0] == 1:
        visit(ms,results)
        return results
    while(True):
        # CASE 0:
        if prefix_len >= len(ms)-1:
            shift_index=len(ms)-1
            insert_index = int( not ms[shift_index] );
        elif ms[prefix_len+1] > ms[prefix_len-1]:
            # first check if we're removing an increase by shifting this left
            # # We create an increase by shifting here: push prefix_len+1 to stack
            # incs.append(prefix_len+1)

            # don't have an increase at prefix_len+1; add one
            if ms[prefix_len+1] <= ms[prefix_len]:
                incs.append(prefix_len+1)

            shift_index = prefix_len
            # we know the number being shifted is positive since it's the first inc
            insert_index = 0

        # CASE 2: ms[i+1] <= ms[i-1]
        else:
            # CASE 2.1 (ms[i+1] != 0) and CASE 2.2.1 (ms[i+1] == 0 and not tight)
            if prefix_sum > prefix_len or ms[prefix_len+1] > 0:
                # Check if we removed an increase 

                if prefix_len < len(ms)-2 and ms[prefix_len+2] > ms[prefix_len+1] and ms[prefix_len+2] <= ms[prefix_len]:
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
                # ms[prefix_len+1] is zero, can't be greater than anything

                shift_index = prefix_len
                # we're shifting first inc, must be greater than 0, so it goes to the front
                insert_index = 0

        ms.insert(insert_index, ms.pop(shift_index))
        if ms[insert_index] < ms[insert_index+1]:
            prefix_sum = ms[0]
            # We already checked for an increase at prefix_len; don't double count
            if insert_index != prefix_len:
                incs.append(insert_index+1)
        else:
            prefix_sum += ms[insert_index]
        visit(ms,results)
        # print(incs)
        if(len(incs) == 0):
            return results
        else:
            prefix_len=incs.pop()

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

def cool_balanced_stack(ms, visit):
    ms.sort(reverse=True)
    results = []
    if ms[0] == 1:
        visit(ms,results)
        return results
    incs = []
    insert_index = 1
    shift_index = len(ms)-1
    ms.insert(insert_index, ms.pop(shift_index))
    # ms.insert(1, ms.pop(len(ms)-1))
    # after this, we know that the first increase is at index 2 if it exists
    prefix_sum = ms[0]
    if ms[1] < ms[2]:
        incs.append(2)
    visit(ms,results)
    while(len(incs) > 0):
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

                # this can't happen: ms[first_inc+1] is zero, can't be greater than anything
                # if ms[first_inc+1] > ms[first_inc]:
                #     incs.pop()
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

def pretty_print_ms_decs(ms,color=True):
    result = "["
    found = 0
    value_colors = [-1] * len(ms)
    decs = []
    for i in range(1, len(ms)):
        index = len(ms)-1-i
        if ms[index] < ms[index+1]:
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
    decs.reverse()
    return decs

def print_usage():
    usage_string ='''Usage: ./balanced_permutations.py [options] frequencies
Frequencies is a list of comma separated frequencies with no spaces

Options:
-l: (l)eft shifts
Generates balanced permutation looplessly using left shifts

-r: (r)ight shifts
Generates balanced permutation looplessly using right shifts

-f: (f)ilter mode
Generates all permutations of the multiset using left and filters to only output the balanced ones. 
Default behavior generates the balanced permutations directly without filtering

-b: filter mode, but using right shifts. badly named option, should be changed

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

-x latex mode
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
                candidate_shifts = find_left_shift(permutations[i-1],perm)
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
                # ind_diff = red_index-candidate_shifts[0][1]
                # preval = permutations[i-1][red_index-1]
                # postval = permutations[i-1][red_index+1]
                # if ind_diff == 0:
                #     print("i",end="\t")
                #     red = True
                # else:
                #     print("i+1",end="\t")
                #     red = False

                # if postval <= preval:
                #     print("LE",end="\t")
                #     le = True
                # else:
                #     print("G",end="\t")
                #     le = False

                # if postval == 0:
                #     print("Z")
                #     z = True
                # else:
                #     print("NZ")
                #     z = False
                
                # if le == False and red == False:
                #     print("This should never occur")
                #     exit(0)

                # print()
            incs = pretty_print_ms(perm, color)
            if len(incs) > 0:
                red_index = incs.pop()
            else:
                red_index = len(ms)-1

def consec_zeroes(ms):
    i = len(ms)-1
    while ms[i] == 0:
        i-=1
    return len(ms)-1-i

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
                # ind_diff = arrow_indices[0]-decs[len(decs)-1]
                # dest_diff = len(perm)-1 - arrow_indices[1]
                # if ind_diff != -1 and ind_diff != 0:
                #     print("unexpected: difference between shifted index and first (from the right) decrease wasn't -0 or -1")
                #     print("pre and post:")
                #     print(prevperm)
                #     print(perm)
                #     print(ind_diff)
                #     # exit(0)
                
                # print("SHIFTED VAL AND DISTANCE FROM END:",prevperm[arrow_indices[0]],dest_diff)
                # if dest_diff != prevperm[arrow_indices[0]]:
                #     print("unexpected: ms[i] wasn't shifted to index len(ms)-1-ms[i]")
                #     print("pre and post:")
                #     print(prevperm)
                #     print(perm)
                #     exit(0)

                # preval = prevperm[decs[len(decs)-1]-1]
                # postval = prevperm[decs[len(decs)-1]+1]
                # if ind_diff == 0:
                #     print("i",end="\t")
                #     red = True
                # else:
                #     print("i-1",end="\t")
                #     red = False

                # if postval <= preval:
                #     print("LE",end="\t")
                #     le = True
                # else:
                #     print("G",end="\t")
                #     le = False
            
                # print()
                # if postval <= preval and ind_diff != -1:
                #     looseness = len(prevperm[decs[len(decs)-1]:]) - sum(prevperm[decs[len(decs)-1]:])
                #     if looseness > prevperm[decs[len(decs)-1]-1]:
                #         print("This should never happen")
                #         exit(0)
                #     # print(len(prevperm[decs[0]:]))
                #     # print(sum(prevperm[decs[0]:]))



                # if postval > preval and ind_diff != 0:
                #     print("This should never happen")
                #     exit(0)

                # print()
            decs = pretty_print_ms_decs(perm, color)




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

def print_ul(perm,scut_ind):
    for i in range(len(perm)):
        p = perm[i]
        if i == scut_ind:
            print("\\underline{",end="")
        print(p,end="")
        if i < len(ms) - 1:
            print(",",end='')
    print("}\\\\")

#dreadfully inefficient but functional
def get_scut_ind(ms):
    reference=sorted(ms,reverse=True)
    scut_ind = len(ms)
    while(scut_ind > 0 and reference[scut_ind-1] == ms[scut_ind - 1]):
        scut_ind -= 1
    scut_ind-=1

    return scut_ind

def print_scuts(permutations,color):
    reference=permutations[len(permutations)-1]
    # print(reference)
    for perm in permutations:
        scut_ind = len(perm)
        while(scut_ind > 0 and reference[scut_ind-1] == perm[scut_ind - 1]):
            scut_ind -= 1
        print_ul(perm,scut_ind)

def formatted_timedelta(delta):
    delta_str = str(delta)
    index = 0
    for i in range(0, len(delta_str)):
        if delta_str[i] != '0' and delta_str[i] != ':':
            index = i
            break

    return delta_str[index:]

def print_debug_reverse(permutations,color):
    permutations.reverse()
    if generate_perms==prefix_direct or generate_perms == prefix_filter:
        print_debug(permutations,color)
    else:
        print_debug_right(permutations,color)

def print_tikzstairs(permutations,color):
    for perm in permutations:
        for val in perm:
            print(val,end="")

        print(" & ",end="")
        print("\\tikzstairs{1,30,0," + str(perm[0]),end="")
        for val in perm[1:]:
            print(", " + str(val),end="")
        print("} \\\\")

if __name__ == "__main__":
    if len( sys.argv ) < 2:
        print_usage()
    else:
        generate_perms=prefix_direct
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
                        if generate_perms==suffix_direct or generate_perms == suffix_filter:
                            output = print_debug_right
                        else:
                            output=print_debug
                    elif argchar == 'i':
                        output=print_debug_reverse
                    elif argchar == 's':
                        output=print_scuts
                    elif argchar == 'f':
                        generate_perms=prefix_filter
                    elif argchar == 'm':
                        generate_perms=prefix_motzkin
                    elif argchar == 'n':
                        color=False
                    elif argchar == 'p':
                        print_only = True
                    elif argchar == 'q':
                        quiet = True
                    elif argchar == 'c':
                        generate_perms=pd_concise
                    elif argchar == 'l':
                        generate_perms=prefix_direct
                    elif argchar == 'r':
                        generate_perms=suffix_direct
                    elif argchar == 'y':
                        generate_perms=cool_dyck
                    elif argchar == 'b':
                        generate_perms=suffix_filter
                    elif argchar == 'a':
                        generate_perms=prefix_general
                    elif argchar == 'e':
                        generate_perms=prefix_lukatex
                    elif argchar == 't':
                        output=print_tikzstairs
                    elif argchar == 'd':
                        diff_mode = True
                    elif argchar == 'x':
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
        for m in ms:
            if m < 0:
                print("Error: Input must not contain negative numbers")

        # if sum(ms) != len(ms) - 1:
        #     exit(1)

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
                # print("Permutations per second, excluding prints:",len(permutations)/total_time)
            print("Total time:",formatted_timedelta(total_time))

