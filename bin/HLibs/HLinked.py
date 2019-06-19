"""This script creates a linked list. This is necessary to dynamically allocate memory for better performance
    This script is created by Hei- Subham Thapa
"""


class Node:
    def __init__(self, Data):
        self.Data = Data
        self.Next = None


class HLinked:
    def __init__(self):
        self.start = None
        self.pointer = None

    def add_node_indexed(self, data, index):
        temp = self.start
        i = 0
        if temp is None:
            self.start = Node(data)
            return
        elif index is 0:
            self.start = Node(data)
            self.start.Next = temp
        else:
            while i < index - 1:
                temp = temp.Next
                i += 1
            node = Node(data)
            node.Next = temp.Next
            temp.Next = node

    def add_node(self, data):
        if self.start is None:
            node = Node(data)
            self.start = node
        else:
            temp = self.start
            while temp.Next is not None:
                temp = temp.Next
            temp.Next = Node(data)

    def del_node(self, index):
        i = 0
        pointer = self.start
        prev = None
        if index is 0:
            self.start = self.start.Next
            return
        while pointer.Next is not None:
            if i is index - 1:
                prev = pointer
            if i is index:
                break
            pointer = pointer.Next
            i += 1
        prev.Next = pointer.Next

    def get_node(self, index):
        i = 0
        temp = self.start
        while i < index:
            if temp is None:
                return False
            temp = temp.Next
            i += 1
        return temp.Data

    def print_val(self):
        temp = self.start
        while temp is not None:
            print temp.Data
            temp = temp.Next
