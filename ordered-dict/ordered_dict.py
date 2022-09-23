class dt_ordered_dict(dict):

    def __init__(self):
        super().__init__(self)
        self.ll = list()

    def add_element(self, a, b):
        self.ll.append(a)
        self[a] = b

    def __str__(self):
        lp = []
        for item in self.ll:
            lp.extend([str(item), ': ', str(self[item]), '\n'])
        ss = ''.join(lp)
        return ss
    
    def items(self):
        def gen_items()
            for item in self.ll:
                yield (item, self[item])
        return get_items

ord_dict = dt_ordered_dict()

ord_dict.add_element('b', 2)
ord_dict.add_element('a', 1)
ord_dict.add_element('aaa', 555)

print("ord_dict[aaa] = {} of type, {}.".format(ord_dict['aaa'], type(ord_dict['aaa'])))
print(str(ord_dict))

for k,v in ord_dict.items():
    print(k, v)


