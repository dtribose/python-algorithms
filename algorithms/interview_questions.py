from __future__ import annotations
# Interview questions by the 15 questions on codementor.io page
# Various extensions from there
import os
import glob
import time
from typing import *
from datetime import datetime, timezone
import random
import re
from collections import namedtuple
from dataclasses import dataclass
import secrets
import heapq



def print_directory_contents(sPath):
    """
    This function takes the name of a directory
    and prints out the paths & files within that
    directory as well as any files contained in
    contained directories.

    Please don't use os.walk in your answer.

    """
    print("\nFiles in directory {}:".format(sPath))
    s_path_ = os.path.join(sPath, '*')
    paths = glob.glob(s_path_)
    dirs = []
    for p in paths:
        if os.path.isfile(p):
            print("\t{}".format(p))
        else:
            dirs.append(p)
    for d in dirs:
        print_directory_contents(d)


def test_directory_printing():
    path_list = ["Users", "David", "dev", "toy-algorithms", "algorithms"]
    s_path = os.path.join("C:\\", *path_list)
    print("\nTarget Path: {}".format(s_path))

    print_directory_contents(s_path)


def test_print_sort_mess():
    # write down the final values of A0, A1, ... An
    # A0 = {'a':1, 'b':2, etc}
    A0 = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))
    print(A0)

    # A1 [0,1,2,3...9]
    A1 = range(10)
    print(list(A1))

    A2 = sorted([i for i in A1 if i in A0])
    # A2 = []
    print(A2)

    # [1,2,3,4,5]
    A3 = sorted([A0[s] for s in A0])
    print(A3)

    ''' # Rest of exercise...
    A4 = [i for i in A1 if i in A3]
    A5 = {i: i * i for i in A1}
    A6 = [[i, i * i] for i in A1]
    '''

class Foo:
    def __init__(self):
        self._bar = 0

    @property
    def bar(self):
        print("Getting bar")
        return self._bar

    @bar.setter
    def bar(self, new_bar):
        self._bar = new_bar
        print('Setting bar to new_bar\n')


def test_at_property():
    foo = Foo()
    print("{}\n".format(foo.bar))
    foo.bar = 3
    print(foo.bar)


def parse_re(input_str):
    """ Use regular expressions to parse the string"""
    vals = re.match("^[-0-9]+", input_str)
    # vals = re.findall("[-0-9]+", input_str)

    code = None
    user_dir = None
    message = None

    if vals:
        code = vals.group(0)
        print(int(code))  # should work since we only searched on 0-9
        message = input_str[len(code):].strip()
        print(f'{message}')

        vals = re.search(r"/jobs/[a-zA-Z0-9]+ ", message)
        if vals:
            user_dir = vals.group(0).strip().split('/')[-1]
            print(user_dir)
    else:
        print('no code found within input string')

    return code, user_dir, message


def test_regular_expression():

    current_time = datetime.now()
    m_string = "-401 My file is /jobs/dtodd in 402 directory foo"
    print(m_string)
    parse_re(m_string)
    code, udir, msg = parse_re(m_string)

    print("'{}', '{}', '{}'".format(code, udir, msg))


def test_regular_expression2():
    str_line = '##INFO=<ID=AA,Number=1.0,Type=String,Description="Ancestral Allele">'

    vals = re.search(r"\A##INFO=<", str_line)
    sp = vals.span()
    sub = str_line[sp[1]:-1]

    # Use re's to search for and then parse particular fields.
    vals = re.search(r"ID=[a-zA-Z]+,", sub)
    sps = vals.span()
    print(sub[sps[0]+3:sps[1]-1])

    # Or select the specific field from the whole string
    ff = re.search(r'(?<=ID=)[a-zA-Z]+(?=,)', sub)
    id_val = ff.group(0)
    print(f"ID_VAL = {id_val}")


    search_patterns = ["Description", "Number", "ID", "Type"] # "ID", "Number", "Type",
    dvals = {}
    for ssp in search_patterns:
        search_string = r'(?<=' + ssp + r'=)[\.a-zA-Z0-9 \"]+(?=,|\Z)'
        ff = re.search(search_string, sub)
        if ff:
            dvals[ssp] = ff.group(0)

    print(dvals)

    sm = 'Description="A Crocker"'
    search_pattern = "Description"
    search_string = r'(?<=' + search_pattern + r'=)[a-zA-Z \"]+(?=,|\Z)'
    fc = re.search(search_string, sm)
    if fc:
        print(fc.group(0))


class DB(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def lookup(self, key):
        print("Doing DB Look-up for key={}".format(key))
        time.sleep(8)
        if key in self:
            return self[key]
        else:
            print("Value not in DB: Going to long term random storage.")
            time.sleep(6)
            return int(round(random.random() * 100.0))

    def add_val(self, key, value):
        print("Adding {}:{} to database".format(key, value))
        self[key] = value


class DllNode(object):
    def __init__(self, key :str, value: int):
        self.key = key
        self.value = value
        self.prev : Any = None
        self.next : Any = None

    def __str__(self):
        return "(%s, %s)" % (self.key, self.value)


db = DB()


class DoublyLinkedList:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Require capacity > 0")
        self.capacity = capacity
        self._size = 0

        # No explicit doubly linked queue here (you may create one yourself)
        self.head :Any = None
        self.tail : Any = None

    def size(self):
        return self._size

    # PUBLIC
    def _set_head(self, node: DllNode):
        if self._size == self.capacity:
            raise Exception("_set_head should only be called after remove.")

        if self.head is None:  # The head does not exist, so neither does the tail
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

        self._size += 1

    def _remove(self, node: DllNode) -> None:
        if not self.head:  # if not head, nothing to remove.
            return

        if node == self.head and node == self.tail:
            self.head = None
            self.tail = None
        elif node == self.head:
            node.next.prev = None
            self.head = node.next
        elif node == self.tail:
            node.prev.next = None
            self.tail = node.prev
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        self._size -= 1

        return

    def add_to_top(self, node: DllNode, in_cache=False):
        remove_key = None
        if self.head == node:
            return remove_key

        if self._size == self.capacity and not in_cache:
            remove_key = self.tail.key
            self._remove(self.tail)
        elif in_cache:
            self._remove(node)

        self._set_head(node)

        return remove_key

    def print_elements(self):
        n = self.head
        print("Head is {}".format(n))
        while n:
            print("{}".format(n))
            n = n.next


class LRUCache(object):
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Require capacity > 0")

        self.hash_map: Dict[str, DllNode] = {}
        self.dll = DoublyLinkedList(capacity)
        self.capacity = capacity

    # PUBLIC

    def get(self, key: str):

        print ("Getting value for key='{}'".format(key))

        if key not in self.hash_map:
            # Then get the value from the "db"
            value = db.lookup(key)
            node = DllNode(key, value)
            removed_key = self.dll.add_to_top(node, in_cache=False)
            if removed_key:
                del self.hash_map[removed_key]
            self.hash_map[key] = node
            return value
        else:
            node = self.hash_map[key]
            self.dll.add_to_top(node, in_cache=True)
            return node.value

    def set(self, key: str, value: int) -> None:
        if key in self.hash_map:
            node = self.hash_map[key]
            # Update value in case it has changed.
            node.value = value

            self.dll.add_to_top(node, in_cache=True)
        else:
            new_node = DllNode(key, value)
            removed_key = self.dll.add_to_top(new_node, in_cache=False)
            if removed_key:
                del self.hash_map[removed_key]

    def print_elements(self):
        self.dll.print_elements()


def test_lru_cache():
    """ Add date to test 'database' then access via cache to speed up"""
    db.add_val('foo', 1)
    db.add_val('bar', 2)
    db.add_val('foobar', 3)
    db.add_val('foozybar', 4)
    db.add_val('boozybar', 5)
    print("\nDB initialization complete\n")

    lru = LRUCache(3)

    lru.print_elements()
    print("Got foo\n", lru.get('foo'))
    print("Got foo\n", lru.get('foo'))
    lru.print_elements()
    print("Got bar\n", lru.get('bar'))
    lru.print_elements()
    print("Got foobar\n", lru.get('foobar'))
    lru.print_elements()
    print("Got bar\n", lru.get('bar'))
    lru.print_elements()
    print("Got foo\n", lru.get('foo'))
    lru.print_elements()
    print("Got boozybar\n", lru.get('boozybar'))
    lru.print_elements()
    print("Got bar\n", lru.get('bar'))
    lru.print_elements()
    print("Got foo\n", lru.get('foo'))
    lru.print_elements()
    print("Got foobar\n", lru.get('foobar'))
    lru.print_elements()
    print("Got coco\n", lru.get('coco'))
    lru.print_elements()


PersonNT = namedtuple('Person', ['name', 'age'])

@dataclass
class PersonS:
    """ Simple person"""
    name: str
    age: int

@dataclass
class Person:
    """ More realistic person with birth date specified"""
    name: str
    birth_date: datetime
    is_alive: bool = True

    @property
    def age(self) -> int:
        now =  datetime.now(tz=timezone.utc)
        age = now - self.birth_date
        return age.days//365


def test_dataclass():

    noah0 = PersonNT('Noah', 81)
    noah1 = PersonS('Noah', 81)
    noah2 = PersonS('Noah', 81)

    noah = Person('Noah', datetime(year=1938, month=9, day=20, tzinfo=timezone.utc))

    print(noah0)
    print(noah1)
    print(noah2)

    print("Noah's age is {}".format(noah.age))
    print(noah)

    print()


# Classes section.
# add type annotations
# add cls members, @classmethod, and @staticmethod.
class A(object):
    def go(self):
        print("go A go!")

    def stop(self):
        print("stop A stop!")

    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")

    def stop(self):
        super(C, self).stop()
        print("stop C stop!")

class D(B, C):
    def go(self):
        super(D, self).go()
        print("go D go!")

    def stop(self):
        super(D, self).stop()
        print("stop D stop!")

    def pause(self):
        print("wait D wait!")

class E(B, C):
    pass


def test_classes():

    a = A()
    b = B()
    c = C()
    d = D()
    e = E()

    # specify output from here onwards

    a.go()
    b.go()
    c.go()
    d.go()
    e.go()

    a.stop()
    b.stop()
    c.stop()
    d.stop()
    e.stop()

    a.pause()
    b.pause()
    c.pause()
    d.pause()
    e.pause()

    pass


def test_secrets():

    print()
    secret = os.urandom(55)  # Old way.
    print("Old urandom = {}".format(secret))
    # New way is better than os.urandom...
    s = secrets.SystemRandom()
    # secret = secrets.SystemRandom.random()
    print("My new secret, s.random()={}".format(s.random()))
    print()


def test_sql_join():

    sql_join_example = \
    """
    SELECT bc.firstname, bc.lastname, b.title, TO_CHAR(bo.orderdate, 'MM/DD/YYYY') "Order Date", p.publishername
    FROM
    BOOK_CUSTOMER bc
    INNER JOIN books b
    ON b.BOOK_ID = bc.BOOK_ID
    INNER JOIN book_order bo
    ON bo.BOOK_ID = b.BOOK_ID
    INNER JOIN publisher p
    ON p.PUBLISHER_ID = b.PUBLISHER_ID
    WHERE p.publishername = 'PRINTING IS US';
    """

class TreeNode():
    def __init__(self, value,
                 parent : Optional["TreeNode"]=None,
                 left_child : Optional["TreeNode"]=None,
                 right_child : Optional["TreeNode"]=None):
        self.value = value
        self.parent = parent
        self.left_child = None
        self.right_child = None
        self.update_children(left_child, right_child)

    def left(self):
        return self.left_child

    def right(self):
        return self.right_child

    def get_parent(self):
        return self.parent

    def set_parent(self, other):
        self.parent = other

    def update_children(self,
                        left_child : Optional["TreeNode"] = None,
                        right_child : Optional["TreeNode"] = None):
        # update parents in children, if left or right not None.
        if left_child:
            self.left_child = left_child
            self.left_child.set_parent(self)
        if right_child:
            self.right_child = right_child
            self.right_child.set_parent(self)

    def depth(self):
        depth = 0
        if self.left() or self.right():
            depth += 1
            ld = 0
            rd = 0
            if self.left():
                ld = self.left().depth()
            if self.right():
                rd = self.right().depth()
            depth += max(ld, rd)
        return depth


def test_binary_tree_size():
    # Create a binary tree.
    one = TreeNode(1)
    two = TreeNode(2)
    ten = TreeNode(10, left_child=one)
    six = TreeNode(6, right_child=two)
    eight = TreeNode(8)
    nine = TreeNode(9)
    seven = TreeNode(7, left_child=eight, right_child=ten)
    three = TreeNode(3, left_child=six, right_child=nine)
    five = TreeNode(5, left_child=three, right_child=seven)

    depth_tree = five.depth()
    print(f"Tree depth = {depth_tree}")

    # add a new zero node to one.
    zero = TreeNode(0)
    one.update_children(right_child=zero)
    depth_tree = five.depth()
    print(f"Updated Tree depth = {depth_tree}")


def heapsort(it : Iterable[Any]):
    h = []
    for v in it:
        heapq.heappush(h, v)
    return [heapq.heappop(h) for i in range(len(h))]


def test_heap_sort():
    ll = [4, 6, -1, 19, -4, 8, 0, 17, 9]
    print(f"Using heapsort to sort the list, {ll}, yeilds:\n{heapsort(ll)}")
    

if __name__ == "__main__":
    # test_directory_printing()
    # test_print_sort_mess()
    # test_at_property()
    # test_regular_expression()
    # test_lru_cache()
    # test_dataclass()
    # test_secrets()

    '''
    # Next two should be tested in more detail
    test_classes()
    test_sql_join()
    '''

    #test_binary_tree_size()
    #test_heap_sort()
    test_regular_expression2()

    pass

