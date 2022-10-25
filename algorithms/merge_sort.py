import time
# import math
# import threading
import multiprocessing as mp
import concurrent.futures as cf
import numpy as np


def sorted_merge(list_a, list_b, f_compare):
    """
    Merges two lists in sorted order

    :param list_a: first list to merge
    :param list_b: second list to merge
    :param f_compare: comparison function to support sorting during merge
    :return:
    """
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
        
        
def merge_sort(list_in, f_compare=(lambda a, b: a < b)):
    """ Sorts list_in using the comparison function f_compare

    :param: list_in: list to be sorted
    :param: f_compare: comparison routine for sorting
    :returns: sorted list
    """
    
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
        list_b = list_in[mid_list:]
        
        list_a = merge_sort(list_a)
        list_b = merge_sort(list_b)
        return sorted_merge(list_a, list_b, f_compare)


def large_merge_sort_mp(list_in, quw=None, new_threads=1, f_compare=(lambda a, b: a < b)):
    """
    Sorts list_in using the comparison function f_compare, and uses multiprocessing if the list is long enough,
    creating max processes equal to number of cpus.

    :param: list_in: list to be sorted
    :param: quw: output queue
    :param: new_threads: current number of threads. It doubles with each call.
    :param: f_compare: comparison routine for sorting
    :returns: sorted list
    """

    new_threads *= 2
    list_len = len(list_in)
    if list_len > 220000 and new_threads <= mp.cpu_count():
        mid_list = list_len // 2
        list_a = list_in[:mid_list]
        list_b = list_in[mid_list:]

        qa = mp.Queue()
        pa = mp.Process(target=large_merge_sort_mp, args=(list_a, qa, new_threads, f_compare))
        pa.start()

        qb = mp.Queue()
        pb = mp.Process(target=large_merge_sort_mp, args=(list_b, qb, new_threads, f_compare))
        pb.start()

        list_a = qa.get()
        list_b = qb.get()
        pa.join()
        pb.join()

    else:
        mid_list = list_len // 2
        list_a = list_in[:mid_list]
        list_b = list_in[mid_list:]

        list_a = merge_sort(list_a)
        list_b = merge_sort(list_b)

    if quw:
        quw.put(sorted_merge(list_a, list_b, f_compare))
    else:
        return sorted_merge(list_a, list_b, f_compare)


def large_merge_sort_cf(list_in, new_threads=1, f_compare=(lambda a, b: a < b)):
    """
    Sorts list_in using the comparison function f_compare, using concurrent.futures for multiprocessing.

    :param: list_in: list to be sorted
    :param: new_threads: current number of threads. It doubles with each call.
    :param: f_compare: comparison routine for sorting
    :returns: sorted list
    """

    new_threads *= 2
    list_len = len(list_in)
    if list_len > 220000 and new_threads <= mp.cpu_count():
        mid_list = list_len // 2
        list_ab = [list_in[:mid_list], list_in[mid_list:]]

        with cf.ProcessPoolExecutor() as executor:
            # * Unfortunately, cannot pass the function f_compare in this routine, since it is not pickleable *
            results = [executor.submit(large_merge_sort_cf, i, new_threads) for i in list_ab]
            result_list = []
            for f in cf.as_completed(results):
                result_list.append(f.result())
            return sorted_merge(result_list[0], result_list[1], f_compare)
    else:
        mid_list = list_len // 2
        list_a = list_in[:mid_list]
        list_b = list_in[mid_list:]

        list_a = merge_sort(list_a)
        list_b = merge_sort(list_b)
        return sorted_merge(list_a, list_b, f_compare)


def merge_sort_test():

    ll_test = [6, 0, 5, 2, 1, 8, 7, 4, 3, 10, -1, 99, 9, -17, 44, -6, 12, 1]

    print("Sorting list: ", ll_test)
    start = time.time()
    sorted_ll = merge_sort(ll_test)
    end = time.time()
    print("Sorted list:  ", sorted_ll)

    print(f"running time was {start-end} seconds")


def large_merge_sort_test():
    ll_test = np.random.randn(500000)
    ll_test *= 500000
    ll_test = ll_test.astype(int).tolist()

    print("\nSorting large list, baseline with regular merge_sort:\n", ll_test[:10])
    start = time.time()
    sorted_ll = merge_sort(ll_test)
    end = time.time()
    print("Sorted large list:  ", sorted_ll[:10])
    print(f"running time was {end - start} seconds")

    print("\n\nSorting large list using concurrent.futures...")
    start = time.time()
    sorted_ll = large_merge_sort_cf(ll_test)
    end = time.time()
    print("Sorted large list:", sorted_ll[:10])
    print(f"running time was {end - start} seconds")

    print("\n\nSorting large list using Multiprocessing: ", ll_test[:10])
    start = time.time()
    sorted_ll = large_merge_sort_mp(ll_test)
    end = time.time()
    print("Sorted large list:  ", sorted_ll[:10])
    print(f"running time was {end - start} seconds")

def concurrent_test():
    import urllib.request
    sleepy_time = 2

    URLS = ['http://www.cnn.com/',
            'http://finance.yahoo.com/',
            'http://www.foxnews.com/',
            'http://www.bbc.co.uk/',
            'http://asjkkksk_567-125_abztcqm.com/']

    def load_url(url, timeout, sleep_time=sleepy_time):
        time.sleep(sleep_time)
        return urllib.request.urlopen(url, timeout=timeout).read()

    with cf.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = dict((executor.submit(load_url, url, 60), url)
                             for url in URLS)

        url_to_result = {}
        for future in cf.as_completed(future_to_url):
            url = future_to_url[future]
            if future.exception() is not None:
                url_to_result[url] = ('e', future.exception())
            else:
                url_to_result[url] = ('r', future.result())

        for url in URLS:
            if url_to_result[url][0] == 'e':
                print('%r generated an exception: %s' % (url, url_to_result[url][1]))
            else:
                print('%r page is %d bytes' % (url, len(url_to_result[url][1])))


if __name__ == "__main__":
    # concurrent_test()
    merge_sort_test()
    large_merge_sort_test()


