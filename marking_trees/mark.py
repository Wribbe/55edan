#!/usr/bin/env python3

import math
import random

MARKED = 'm'
UNMARKED = 'u'

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

def has_children(index, tree):
    return [i for i in children(index) if i < len(tree)]

def marked(index, tree):
    return tree[index] == MARKED

def mark(index, tree):
    """ Apply marking rules and return nodes that should be marked in the
    future.

    Rules:
        - If parent and sibling to a node is marked, mark node.
        - If both children to node are marked, mark node.
    """
    to_be_marked = []
    tree[index] = MARKED

    if has_children(index, tree):

        child_left, child_right = children(index)

        marked_left = marked(child_left, tree)
        marked_right = marked(child_right, tree)

        if marked_left and not marked_right:
            to_be_marked.append(child_right)
        elif marked_right and not marked_left:
            to_be_marked.append(child_left)

    if index > 0: # Not in root node.

        index_parent = parent(index)
        index_sibling = sibling(index)

        marked_parent = marked(index_parent, tree)
        marked_sibling = marked(index_sibling, tree)

        if not marked_parent and marked_sibling:
            to_be_marked.append(index_parent)
        elif not marked_sibling and marked_parent:
            to_be_marked.append(index_sibling)

    return to_be_marked

def mark_tree(value, tree):
    mark_queue = [value] if not marked(value, tree) else []
    n_marked = 0

    while mark_queue:
        index_to_mark = mark_queue.pop(0)
        if marked(index_to_mark, tree):
            continue
        mark_queue += mark(index_to_mark, tree)
        n_marked += 1
    return n_marked

def R1(N):
    return random.randint(0,N-1)

def R2(stored):
    return stored.pop()

def R3(stored, tree):
    index = stored.pop()
    while marked(index, tree):
        index = stored.pop()
    return index

def run(index_generator, generator_input, tree):
    iterations = 0
    n_marked = len([node for node in tree if node == MARKED])
    while n_marked != len(tree):
        iterations += 1
        # The pattern `function(*[list, of, vars])` is equal to the following
        # call:
        #   function(list, of, vars)
        next_index = index_generator(*generator_input)
        n_marked += mark_tree(next_index, tree)
    return iterations

def main():
    h_max = 20
    h_start = 2
    for h in range(h_start,h_max+1):
        N = int(math.pow(2,h)-1)
        print("h={},N={}".format(h,N))
        # Setup for R1.
        tree = [UNMARKED] * N
        R1_iterations = run(R1, [N], tree)
        print("  R1 - iterations: {}".format(R1_iterations))

        # Setup for R2.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R2_iterations = run(R2, [stored], tree)
        print("  R2 - iterations: {}".format(R2_iterations))

        # Setup for R3.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R3_iterations = run(R3, [stored, tree], tree)
        print("  R3 - iterations: {}".format(R3_iterations))
        print()

def test_example():
    example_tree = [
            MARKED, UNMARKED, UNMARKED, MARKED, UNMARKED, MARKED, UNMARKED
            ]

    # Example tree from paper, should complete in one round.
    return_value = lambda x: x # Returns input value.
    iterations = run(return_value, [4], example_tree)
    if not iterations == 1:
        print("Example tree should complete in one iteration " +\
              "with R1 and input-index 4, aborting. ")
        return False
    return True

if __name__ == "__main__":
    if test_example():
        main()
    else:
        print("Test example failed. Abort.")
