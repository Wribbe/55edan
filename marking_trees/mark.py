#!/usr/bin/env python3

import math
import random

MARKED = 'm'
UNMARKED = 'u'

example_tree = [MARKED, UNMARKED, UNMARKED, MARKED, UNMARKED, MARKED, UNMARKED]

def sibling(index):
    if index%2 == 0:
        return index-1
    return index+1

def parent(index):
    half_index = int(index/2)
    if index%2 == 0:
        return half_index-1
    return half_index

def children(index):
    left_child = (index*2)+1
    right_child = left_child+1
    return [left_child, right_child]

def mark(index, tree):
    tree[index] = MARKED

def marked(index, tree):
    if type(index) == list:
        return all([marked(ind, tree) for ind in index])
    if index > len(tree)-1 or index < 0:
        return False
    return tree[index] == MARKED

def marking_rule(index, tree):

    # 1. An internal node gets marked when both its children are marked.
    # 2. A non-root node gets marked if its parent and sibling are marked.
    if marked(children(index), tree):
        return True
    elif marked([parent(index), sibling(index)], tree):
        return True

def R1(N):
    return random.randint(1,N-1)

def R2(N, stored):
    return stored.pop()

def R3(N, stored, tree):
    index = stored.pop()
    while tree[index]:
        index = stored.pop()
    return index

def traverse_marking_rule(index, tree, visited):
    if index < 0 or index > len(tree)-1 or visited[index]:
        return 0
    num_marked = 0
    visited[index] = True
    if not marked(index, tree) and marking_rule(index, tree):
        mark(index, tree)
        num_marked += 1

    left, right = children(index)
    num_marked += traverse_marking_rule(left, tree, visited)
    num_marked += traverse_marking_rule(right, tree, visited)

    num_marked += traverse_marking_rule(parent(index), tree, visited)
    return num_marked

def mark_tree(tree, function, function_input, predefined_indexes=[]):

    N = len(tree)
    num_marked = len([val for val in tree if val == MARKED])
    rotations = 0
    while num_marked != N:
        if predefined_indexes:
            new_index = predefined_indexes.pop()
        else:
            new_index = function(*function_input)
        if not marked(new_index, tree):
            mark(new_index, tree)
            num_marked += 1
            num_marked += traverse_marking_rule(new_index, tree, [False] * N)
        rotations += 1
    return rotations
rotations = mark_tree(example_tree, R1, [len(example_tree)], [4])
print(rotations)
