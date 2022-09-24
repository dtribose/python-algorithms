import multiprocessing as mp
import numpy as np
import time
import timeit
import os

n_cpu = mp.cpu_count()
print(f"number of cpus = {n_cpu}")

# big_array = []
# for i in range(3):
#     big_array.append(list(np.random.randn(10000000) * 100.))

"""
If passing around large amounts of data
it will need to be pickled and un-pickled,
which will take some time, and may eliminate
the benefit of multiprocessing. However, if
the data passed is small and the time occupied
is large it will work every effectively.
"""


def square(x):
    return x*x


def wait_time(x):
    print(f"sleeping: x = {x}")
    time.sleep(7)


def p_square(val):
    """Squares all values if x is a list"""
    with mp.Pool(3) as p:
        # return p.map(square, val)
        return p.map(wait_time, val)


def info_title(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print()
    time.sleep(7)


def test_001():
    xx = [1, 2, 3]
    start1 = time.time()
    foo = list(p_square(xx))
    # foo = list(map(wait_time, xx))
    # foo = list(p_square(big_array[1]))
    # foo = list(map(square, big_array[1]))
    end1 = time.time()
    print(f"elapsed time = {end1 - start1}")
    # print(foo[:5])
    # print(len(foo))


def test_002(names):
    pp = []
    for i, n in enumerate(names):
        pp.append(mp.Process(target=info_title, args=(n,)))
        pp[i].start()

    time.sleep(.01)
    print("waiting for jobs to finish...")
    for p in pp:
        p.join()


if __name__ == "__main__":
    # test_001()
    name_list = ["billy", "suzie", "porsche", "jill"]
    start = time.time()
    test_002(name_list)
    # for _, name in enumerate(name_list):
    #     info_title(name)
    end = time.time()
    print(f"elapsed time = {end - start}")
