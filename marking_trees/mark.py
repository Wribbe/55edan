#!/usr/bin/env python3

import math
import random

MARKED = 'm'
UNMARKED = 'u'

def main():
    start_h = 2
#    max_h = 20
    max_h = 4
    tree = []
    visited = []

    def get_tree(N):
        return ([False]*N, [UNMARKED]*N)

    def even(value):
        return value%2 == 0

    def parent(index):
        if even(index):
            return int((index/2)-1)
        return int(index/2)

    def sibling(index):
        if even(index):
            return index-1
        return index+1

    def children(index):
        first = index*2+1
        second = first+1
        return [first, second]

    def mark1(index):
        mark(index-1)

    def mark(index):
        tree[index] = MARKED;

    def marked(index):
        if type(index) == list:
            return all([marked(ind) for ind in index])
        if index > len(tree)-1:
            return False
        return tree[index] == MARKED

    def execute_rule(index):
        if type(index) == list:
            for ind in index:
                execute_rule(ind)
        else:
            if index > len(tree)-1 or visited[index]:
                return
            if marked(children(index)) or \
               marked([parent(index), sibling(index)]):
                mark(index)

            visited[index] = True
            execute_rule(parent(index)) # Travel upwards.
            execute_rule(children(index)) # Travel downwards.

    def all_marked():
        return all([node == MARKED for node in tree])

    for h in range(start_h, max_h+1):
        N = int(math.pow(2, h)-1)
        visited, tree = get_tree(N)
        if N == 7:
            mark1(1)
            mark1(4)
            mark1(6)
            print(tree)
            print(all_marked())
            mark1(5)
            execute_rule(4)
            print(tree)
            print(all_marked())

if __name__ == "__main__":
    main()
