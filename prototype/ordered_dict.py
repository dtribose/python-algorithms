class dt_ordered_dict(dict):

    def __init__(self):
        super().__init__(self)
        self.ordered_keys = list()

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, val):
        self._add_element(key, val)

    def _add_element(self, a, b):
        if a not in self.ordered_keys:
            self.ordered_keys.append(a)
        super().__setitem__(a, b)

    def __repr__(self):
        return "Ordered version of: {}".format(super().__repr__())

    def __str__(self):
        lp = []
        for key in self.ordered_keys:
            lp.append("{}: {}".format(key, self[key]))
        ss = ', '.join(lp)
        return "{" + ss + "}"
    
    def iteritems(self):
        for key in self.ordered_keys:
            yield (key, self[key])


if __name__ == "__main__":

    ord_dict = dt_ordered_dict()

    ord_dict['c'] = 2
    ord_dict['a'] = 1
    ord_dict['aaa'] = 555
    ord_dict['b'] = 33
    ord_dict['aaa'] = 17

    print("ord_dict['aaa'] = {} of type, {}.".format(ord_dict['aaa'], type(ord_dict['aaa'])))
    print("str(ord_dict) = {}".format(str(ord_dict)))
    print("repr(ordered_dict) = {}".format(repr(ord_dict)))
    print('\n')

    for k,v in ord_dict.iteritems():
        print(k, v)


