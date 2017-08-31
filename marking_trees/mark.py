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
    return random.randint(0,N-1)

def R2(stored):
    return stored.pop()

def R3(stored, tree):
    index = stored.pop()
    while marked(index, tree):
        index = stored.pop()
    return index

def iterative_marking_rule(index, tree, visited, initial_state=None):
    if index < 0 or index > len(tree)-1 or visited[index]:
        return 0
    num_marked = 0
    visited[index] = True
    if not initial_state:
        initial_state = tree[index]
    if not marked(index, tree) and marking_rule(index, tree):
        mark(index, tree)
        num_marked += 1

    # No need to traverse upwards, downwards or signal sibling if there was no
    # state change.
    if (initial_state != tree[index]):
        num_marked += iterative_marking_rule(parent(index), tree, visited)
        num_marked += iterative_marking_rule(sibling(index), tree, visited)
        if not marked(children(index), tree):
            left, right = children(index)
            num_marked += iterative_marking_rule(left, tree, visited)
            num_marked += iterative_marking_rule(right, tree, visited)
    return num_marked

def mark_tree(tree, function, function_input, input_indexes=[]):

    N = len(tree)
    num_marked = len([val for val in tree if val == MARKED])
    iterations = 0
    while num_marked != N:
        if input_indexes:
            new_index = input_indexes.pop()
        else:
            new_index = function(*function_input)
        if not marked(new_index, tree):
            num_marked += 1
            mark(new_index, tree)
            num_marked += iterative_marking_rule(new_index, tree, [False] * N,
                    UNMARKED)
        iterations += 1
        dynamic_status = "INFO: Current iteration: {}\r".format(iterations)
        print(dynamic_status, end="")
    # Clear the current iteration print.
    print("{}\r".format(" "*len(dynamic_status)), end="")
    return iterations

def main():

    # Example tree from paper, should complete in one round.
    iterations = mark_tree(example_tree, R1, [len(example_tree)], [4])
    if not iterations == 1:
        print("Example tree should complete in one iteration " +\
              "with R1 and input-index 4, aborting. ")
        return

    h_max = 20
    h_start = 2
    for h in range(h_start,h_max+1):
        N = int(math.pow(2,h)-1)
        print("h={},N={}".format(h,N))
        # Setup for R1.
        tree = [UNMARKED] * N
        R1_iterations = mark_tree(tree, R1, [N])
        print("  R1 - iterations: {}".format(R1_iterations))

        # Setup for R2.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R2_iterations = mark_tree(tree, R2, [stored])
        print("  R2 - iterations: {}".format(R2_iterations))

        # Setup for R3.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R3_iterations = mark_tree(tree, R3, [stored, tree])
        print("  R3 - iterations: {}".format(R3_iterations))
        print()

if __name__ == "__main__":
    main()
