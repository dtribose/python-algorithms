# Creating my own ordered dict class.
# This currently keeps a list and makes sure it is sorted, however it is not the fastest approach.
# It should be possible to put items in a tree structure and O(log(n)) insertion time instead od O(n),
# That is assuming items are entered at random.

class dt_ordered_dict(dict):

    def __init__(self):
        super().__init__(self)
        self.ll = list()

    def add_element(self, k, v, verbose=False):
        self.ll.append(k)
        self.ll.sort()  # Make sure this is kept sorted (ordered).
        self[k] = v
        if verbose:
            print(f"adding new key:value pair, {k}:{v}")

    def __str__(self):
        lp = []
        for item in self.ll:
            lp.extend([str(item), ': ', str(self[item]), '\n'])
        ss = ''.join(lp)
        return ss
    
    def items(self):
        def gen_items():
            for item in self.ll:
                yield item, self[item]
        return gen_items()


def test_ordered_dict():
    ord_dict = dt_ordered_dict()
    print()
    ord_dict.add_element('b', 2, verbose=True)
    ord_dict.add_element('a', 1, verbose=True)
    ord_dict.add_element('d', 347, verbose=True)
    ord_dict.add_element('aaa', 555, verbose=True)
    ord_dict.add_element('bb', -17, verbose=True)

    print(f"\nConfirmed, ord_dict[aaa] = {ord_dict['aaa']} of type {type(ord_dict['aaa'])}.")
    print("\ndictionary_contents:")
    print(str(ord_dict))

    # Using ord_dict.items() method.
    print("Using ord_dict.items() method:")
    for k, v in ord_dict.items():
        print(k, v)


if __name__ == "__main__":

    test_ordered_dict()