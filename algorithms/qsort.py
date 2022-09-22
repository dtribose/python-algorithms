# Qsort algorithm

# Does this work?

def qsort(unsorted_list):
    # find median value of first, last, and middle point

    def swap_val(ll, i, j):
        temp = ll[i]
        ll[i] = ll[j]
        ll[j] = temp
        return

    # Use the real mean not just the middle one @@@
    def mean_ix(ll, triple):
        ix0 = triple[0]
        ix1 = triple[1]
        ix2 = triple[2]
        a = ll[ix0]
        b = ll[ix1]
        c = ll[ix2]

        if a < b:
            if c < a:
                return ix0
            elif c > b:
                return ix2
            else:
                return ix1
        else: # b < a
            if c < b:
                return ix1
            elif c > a:
                return ix0
            else:
                return ix2

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


llt = [6, 0, 3, 5, 2, 7, 9, 8, 1, 11, 15, 12, 14, 16, -1]
qsort(llt)
print(llt)
