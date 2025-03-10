# Qsort algorithm
from collections import deque
import numpy as np


def simple_quick_sort(unsorted):
    """ Simple and non-in-place sorting algorithm to demonstrate some of the
    key qualities of quicksort.
    :param unsorted: List to sort
    :return: Sorted list
    """

    if len(unsorted) < 2:
        return unsorted
    pivot = unsorted[-1]

    vals_above = []
    vals_below = []

    for v in unsorted[:-1]:
        if v <= pivot:
            vals_below.append(v)
        else:
            vals_above.append(v)

    return simple_quick_sort(vals_below) + [pivot] + simple_quick_sort(vals_above)


def hoare_quicksort(unsorted):
    """ An in place implementation of the Hoare version of quicksort.
        Uses the right most value (with the largest index) as the pivot.

    :param unsorted: List to be sorted
    :return: None, after the list is sorted
    """

    def swap_val(ll, i, j):
        lli_temp = ll[i]
        ll[i] = ll[j]
        ll[j] = lli_temp
        return

    def sort_quick(ll, lo, hi):
        """ Subroutine that is called recursively to sort the current list or its sub-lists.
            Sorts ll over the range from lo to hi in place.

        :param ll: list to sort
        :param lo: lowest index to sort
        :param hi: highest index to sort
        :return:
        """
        length = hi - lo + 1
        if length < 2:
            return
        elif length == 2:
            if ll[lo] > ll[hi]:
                swap_val(ll, lo, hi)
            return

        ipivot = hi
        pivot = ll[ipivot]
        ilo = lo
        ihi = hi - 1

        insert_pivot = None
        while True:
            while ll[ilo] <= pivot and ilo < ihi:
                ilo += 1
            if ilo < ihi:
                while ll[ihi] > pivot and ihi > ilo:
                    ihi -= 1
                if ihi > ilo:
                    swap_val(ll, ilo, ihi)
                    insert_pivot = ihi
                else:
                    if ll[ihi] > pivot:
                        insert_pivot = ihi
                    break
            else:
                # print(f"ilo, insert_pivot, ipivot = {ilo}, {insert_pivot}, {ipivot}")
                if ll[ilo] > pivot:
                    insert_pivot = ilo
                break

        if insert_pivot is not None:
            swap_val(ll, insert_pivot, ipivot)

            sort_quick(ll, lo, insert_pivot-1)
            sort_quick(ll, insert_pivot+1, hi)
        else:
            sort_quick(ll, lo, hi-1)

    sort_quick(unsorted, 0, len(unsorted)-1)


def qqsort(unsorted_list, pivot_threshold_count=None):
    """ Older version of quicksort for sorting in-place.

    :param unsorted_list: List to sort
    :param pivot_threshold_count: Threshold of length before subroutine checks three values to find the best pivot.
    :return: None, after list is sorted.
    """

    if not pivot_threshold_count:
        pivot_threshold_count = 34

    def swap_val(ll, i, j):
        lli_temp = ll[i]
        ll[i] = ll[j]
        ll[j] = lli_temp
        return

    # Use the real mean not just the middle one @@@
    def mean_ix(ll, triple):
        """ Find best of 3 values to use for sorting.

        :param ll: list being sorted
        :param triple: tuple of three indices - of the first, middle, and last value
        :return: index of the middle of the three values
        """
        first, second, third = triple
        a = ll[first]
        b = ll[second]
        c = ll[third]

        if a <= b:
            if c <= a:
                return first
            elif b <= c:
                return second
            else:
                return third
        else:  # b < a
            if c <= b:
                return second
            elif a <= c:
                return first
            else:
                return third

    def sort_quick(ll, min_, max_):
        """ Subroutine for quickly sorting an array.
        Uses a queue to hold index value for values that are > pivot.
        Sorts ll in place from index min_ to max_.

        :param ll: list or sub-list to sort
        :param min_: lowest index for sort
        :param max_: upper index for sort
        :return: None, after ll is sorted
        """

        ulen = max_ - min_ + 1

        # Will never enter is ulen = 0 or 1
        if ulen == 2:
            if ll[min_] > ll[max_]:
                swap_val(ll, min_, max_)
            return
        elif ulen > pivot_threshold_count:
            pivot_ = mean_ix(ll, (min_, max_, (min_ + max_) // 2))
            swap_val(ll, max_, pivot_)

        pivot = border = max_
        pivot_value = ll[pivot]

        swap_index = deque()
        ii = min_
        while ii < max_:
            if ll[ii] > pivot_value:
                swap_index.append(ii)
            elif len(swap_index):
                swap_val(ll, ii, swap_index.popleft())
                swap_index.append(ii)
            ii += 1

        if len(swap_index):
            border = swap_index.popleft()
            swap_val(ll, pivot, border)

        del swap_index

        if border-1 - min_ > 0:  # ulen > 1
            sort_quick(ll, min_, border-1)
        if max_ - (border+1) > 0:
            sort_quick(ll, border+1, max_)

    sort_quick(unsorted_list, 0, len(unsorted_list) - 1)


def is_sorted(ll):
    for i in range(len(ll) - 1):
        if not ll[i] <= ll[i + 1]:
            return False
    return True


def run_test1():
    ll = [120, 6, 0, 3, 5, -2, 7, 9, 8, 1, -11, 15, 12, 2, 14, 16, -1, 4]
    print(f"Original unsorted list is: {ll}")
    qqsort(ll, pivot_threshold_count=12)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + " is " + iss + "sorted")


def run_test2():
    ll = [14, 12, 10, 8, 6, 4, 2, 0, -1, -2, -3, -4, -5, -6, -7]
    print(f"Original unsorted list is: {ll}")
    qqsort(ll, pivot_threshold_count=9)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + " is " + iss + "sorted")


def run_test3():
    ll = [1, 8, 7, -11, -2, 5, 4, 16, 15, -5, -6, 3, 2]
    print(f"Original unsorted list is: {ll}")
    qqsort(ll)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + " is " + iss + "sorted")


def run_test4():
    ll = np.random.rand(1000) * 10000.0
    ll = ll.astype(dtype=np.int32)
    ll = ll.tolist()
    print(f"Original unsorted list is: {ll}")
    qqsort(ll)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + "\n is " + iss + "sorted")


def run_test_sqs1():
    ll = [1, 8, 7, -11, -2, 5, 4, 16, 15, -5, -6, 3, 2, -7, 18, 0]
    print(f"Original unsorted list is: {ll}")
    ll = simple_quick_sort(ll)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + " is " + iss + "sorted")


def run_test_hoare():
    # ll = [1, 8, 7, -11, -2, 5, 4, 16, 15, -5, -6, 3, 2]
    ll = [-7, -133, -41, -7, -111, 33, 0, 26, -37, -265]
    print(f"Original unsorted list is: {ll}")
    hoare_quicksort(ll)
    iss = "" if is_sorted(ll) else "not "
    print(str(ll) + " is " + iss + "sorted")


def run_hoare_longtest():
    ll = np.random.randn(1000) * 10000.0
    ll = ll.astype(dtype=np.int32)
    ll = ll.tolist()
    print(f"Original unsorted list is: {ll}")
    hoare_quicksort(ll)
    # print(f"results: {ll}")
    iss = "" if is_sorted(ll) else "not "
    print("results: " + str(ll) + "\n is " + iss + "sorted")


if __name__ == "__main__":
    run_test1()
    print("done with test 1\n")
    run_test2()
    print('done with test 2\n')
    run_test3()
    print('done with test 3\n')
    # run_test4()  # bigger test
    # print('done with test 4\n')

    run_test_sqs1()
    print("done with tests sqs-1\n")

    run_test_hoare()
    print('done with test hoare\n')

    run_hoare_longtest()
    print('done with hoare longtest\n')

    x = 1

