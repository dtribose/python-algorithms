# Qsort algorithm

def qsort(unsorted_list):
    # find median value of first, last, and middle point

    def swap_val(l, i, j):
        xi = l[i]
        l[i] = l[j]
        l[j] = xi
        return

    # Use the real mean not just the middle one @@@
    def mean_ix(l, triple):
        first = triple[0]
        second = triple[1]
        third = triple[2]
        a = l[first]
        b = l[second]
        c = l[third]

        if a < b:
            if c < a:
                return first
            elif c > b:
                return third
            else:
                return second
        else: # b < a
            if c < b:
                return second
            elif c > a:
                return first
            else:
                return third

    def sort_quick(unsorted, min, max):

        ll = unsorted

        ulen = max - min + 1

        if ulen <= 1:  # @@@ can the number of points equal zero?
            return
        elif ulen == 2:
            if ll[min] < ll[max]:
                return
            else:
                swap_val(ll, min, max)
                return
        else:
            pivot = mean_ix(ll, (min, max, (min + max) // 2))
            pv = ll[pivot]
            print("pivot value = {}".format(pv))
            if pv == 8:
                x = 0
            swap_val(ll, min, pivot)
            border = min + 1
            while ll[border] < pv and border < max+1:
                border += 1

            for i in range(border + 1, max + 1):
                if ll[i] < pv:
                    swap_val(ll, border, i)
                    border += 1
            else:
                border = border-1

            swap_val(ll, border, min)

            sort_quick(ll, min, border-1)
            sort_quick(ll, border+1, max)

            return

    return sort_quick(unsorted_list, 0, len(unsorted_list) - 1)


ll = [6, 0, 3, 5, 2, 7, 9, 8, 1, 11, 15, 12, 14, 16, -1]
qsort(ll)
print(ll)