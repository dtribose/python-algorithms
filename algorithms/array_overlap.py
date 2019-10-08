import numpy as np


def array_overlap(a, b, preserve_order=True):
    """ return the sub-set of ints in a that are also in b

    a: input numpy array
    b: input numpy array
    preserve_order: specified if the order of values in returned array
                    should be the same as order in a.
    return: array of values in a that are also in b
    """

    if not preserve_order:
        aset = set(a)
        bset = set(b)
        cset = aset & bset
    else:
        bsorted = np.array(sorted(list(set(b))))
        axsorted = np.array(sorted(zip(a,range(0,len(a)))))
        asorted = np.array(sorted(a))

        len_aa = len(aa)
        cset = []
        ax = 0
        for bb in bsorted:
            # ... still not quite right as
            # values in b are not what's being added...
            aix = np.searchsorted(asorted[ax:], bb)
            ax = ax + aix
            if ax > len_aa - 1:
                break
            else:
                # If multiple 'a' entries that match.
                while bb == asorted[ax] and bb == axsorted[ax][0]:
                    cset.append(axsorted[ax])
                    ax = ax + 1

        cset.sort(key=lambda x: x[1])
        cset = np.array((cset))[:,0]

    return cset


if __name__ == "__main__":

    aa = np.array([1,3,6,-20,99,15,0,-12,9, 49, -7, 4,4,87,85,43,22,-21,18])

    bb = np.array([49,4,4,4,4,5,0,22,9,33,44,88,10, 87,0,5])

    # cc = array_overlap(aa, bb, preserve_order=False)
    # assert(set(cc) == set((0,4,9,22,49,87)))

    cc = array_overlap(aa, bb)
    assert(np.all(cc == [0,9,49,4,4,87,22]))

    print("\nSub-array of aa that is also in bb: {}".format(cc))