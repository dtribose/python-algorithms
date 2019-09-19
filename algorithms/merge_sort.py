import time
import math


# in place OR copy and return sorted.

# lts ==> list to sort
def bad_sort(lts, compare):

    s_list = list(lts)
      
    slen = len(s_list)
    if slen < 2:
        return s_list

    sorted = False
    while not sorted:
        for a in lts:
            for b in lts[a:]:
                if compare(a,b) == False:
                    cc = b
    # ....


def sorted_merge(list_a, list_b, f_compare):
    list_new = []

    ib_start = 0
    ia_start = 0
    len_b = len(list_b)
    len_a = len(list_a)
    
    for ia in range(ia_start, len_a):
        for ib in range(ib_start, len_b):
            if f_compare(list_a[ia], list_b[ib]):
                list_new.append(list_a[ia])
                ia_start += 1
                break
            else:
                list_new.append(list_b[ib])
                ib_start += 1

    if ia_start < len_a:
        for ia in range(ia_start, len_a):
            list_new.append(list_a[ia])
    elif ib_start < len_b:
        for ib in range(ib_start, len_b):
            list_new.append(list_b[ib])
    
    return list_new
        
        
def merge_sort(list_in, f_compare=(lambda a,b: a < b)):
    
    list_len = len(list_in)
    if list_len < 2:
        return list_in
    if list_len == 2:
        if not f_compare(list_in[0], list_in[1]):
            return [list_in[1], list_in[0]]
        else:
            return list_in
    else:
        mid_list = list_len//2
        list_a = list_in[:mid_list]
        #print list_a
        list_b = list_in[mid_list:]
        #print list_b
        list_a = merge_sort(list_a)
        list_b = merge_sort(list_b)

        return sorted_merge(list_a, list_b, f_compare)


def merge_sort_test():
    print ("About to sort list: ", ll_test)

    sorted_ll = merge_sort(ll_test)

    print("Sorted list: ", sorted_ll)


if __name__ == "__main__":

    ll_test = [6,5,2,1,8,7,4,3,10,9]

    merge_sort_test()
    
