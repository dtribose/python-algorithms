# Build a tree structure
# Have it double in size on every level
# have the value of every node equal to the hash of the sum of hashes of the two children nodes
# If a leaf node is initialized with no value make it zero.
# If a leaf node is initialized with a value, it's stored value will be the hash of that value.
# This is a sparse tree and we want to initialize it to 64 levels.
# Only store nodes that are not initialized with zero.
# Create an update script so that updating a leaf node updates all the parents.

import numpy as np
from collections import OrderedDict


def hash_func(val):
    if val == 0:
        return 0
    else:
        val = round((val * 1234567.89) % 131, 14)  # Guess as to what will be good.
        return val


class Node_:
    hash = None

    @classmethod
    def set_hash(cls, func):
        cls.hash = func

    def __init__(self, value=None, depth=None, index=None):
        if depth is None or index is None:
            raise AttributeError("Depth and index must be 0 or greater and cannot be None")
        if value is None or value == 0:
            self.value = 0
        else:
            self.value = Node_.hash(value)
        self.depth = depth
        self.index = index

    def get_value(self):
        return self.value

    def update(self, value):
        self.value = Node_.hash(value)
        return self.value

    def update_node(self, value1, value2):
        self.value = Node_.hash(value1 + value2)
        return self.value


class SparseTree:
    layers = []  # hold ordered-dict.

    def __init__(self, initial_depth=0, hash_function=lambda x: x + 1):
        Node_.set_hash(hash_function)
        # create the root Node.
        self.layers.append(OrderedDict({0: Node_(None, 0, 0)}))
        self.depth = initial_depth
        if initial_depth > 0:
            for i in range(1, initial_depth + 1):
                self.layers.append(OrderedDict())

    def _add_node(self, value, depth, index):
        if index > 2**depth - 1:
            return 2, "Adding node failed - as index is > 2**depth - 1"
        if depth > self.depth + 1:
            return 1, "Adding node failed : depth exceeds self.depth+1"
        elif depth == self.depth + 1:
            self.layers.append(OrderedDict())
            self.depth = depth
        self.layers[depth][index] = Node_(value, depth, index)
        return 0, "" 

    def update_leaf_node(self, value, depth, index):
        if index > 2**depth - 1:
            return 2, "Updating node failed - as index is > 2**depth - 1"
        if depth > self.depth:
            return 1, "Adding node failed : depth exceeds self.depth+1"
        else:
            node = self.layers[depth].get(index, None)
            if node is None and value == 0:
                # Nothing to do.
                return 0, ""
            elif value == 0:
                # delete this node and go back to no entry.
                self.layers[depth].delete(index)
            elif node is None:
                _, _ = self._add_node(value, depth, index)
                value = self.layers[depth].get(index).get_value()
            else:
                value = node.update(value)  # If value is zero - need to create.
        self._update_parents(value, depth, index)
        return 0, ""

    def _update_parents(self, value, depth, index):
        while depth > 0:
            # parent is depth-1, index//2
            parent_depth = depth - 1
            parent_index = index // 2
            # get value from sister node:
            if index % 2 == 0:
                sister_index = index + 1
            else:
                sister_index = index - 1
            value2 = self.layers[depth].get(sister_index, 0)
            if value2 != 0:
                value2 = value2.get_value()
            parent_node = self.layers[parent_depth].get(parent_index, None)
            if parent_node is None:
                self._add_node(value + value2, parent_depth, parent_index)
                value = self.layers[parent_depth][parent_index].get_value()
            else:
                value = parent_node.update_node(value, value2)
            index = parent_index
            depth = parent_depth

    def get_node_value(self, depth, index):
        node = self.layers[depth].get(index, None)
        if node is None:
            return 0
        else:
            return node.get_value()


if __name__ == "__main__":
    st = SparseTree(initial_depth=4, hash_function=hash_func)
    (code, error) = st.update_leaf_node(33, 4, 4)
    print(f"Value of root node after update = {st.get_node_value(0, 0)}")

    (code, error) = st.update_leaf_node(2, 4, 9)
    print(f"Value of root node after update = {st.get_node_value(0, 0)}")

    x = 0
