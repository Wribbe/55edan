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
    return tree[index][0] == MARKED

def mark(index, tree):
    # Collect and return cascade markings that should be made due to marking
    # index.
    cascade = []
    tree[index] = (MARKED, tree[index][1])
    if has_children(index, tree):
        child = children(index)
        if marked(child[0], tree) and not marked(child[1], tree):
            cascade += [child[1]]
        elif marked(child[1], tree) and not marked(child[0], tree):
            cascade += [child[0]]

    if index > 0:
        if marked(sibling(index), tree) and not marked(parent(index), tree):
            cascade += [parent(index)]
        elif marked(parent(index), tree) and not marked(sibling(index), tree):
            cascade += [sibling(index)]
    return cascade

def mark_tree(value, tree):
    mark_queue = [value] if not marked(value, tree) else []
    n_marked = 0
    while mark_queue:
        sub_queues = [mark(i, tree) for i in mark_queue if not marked(i, tree)]
        n_marked += len(sub_queues)
        mark_queue = [index for sub_queue in sub_queues for index in sub_queue]
    return n_marked

def R1(N):
    return random.randint(0,N-1)

def R2(stored):
    return stored.pop()

def R3(tree):
    def lam(stored):
        index = stored.pop()
        while marked(index, tree):
            index = stored.pop()
        return index
    return lam

def run(index_generator, seed, tree):
    iterations = 0
    n_marked = sum([1 for i in range(0, len(tree)) if marked(i, tree)])
    while n_marked != len(tree):
        iterations += 1
        n_marked += mark_tree(index_generator(seed), tree)
    return iterations

def main():
    h_max = 20
    h_start = 2
    for h in range(h_start,h_max+1):
        N = int(math.pow(2,h)-1)
        print("h={},N={}".format(h,N))
        # Setup for R1.
        tree = [(UNMARKED, i) for i in range(0, N)]
        R1_iterations = run(R1, N, tree)
        print("  R1 - iterations: {}".format(R1_iterations))

        # Setup for R2.
        tree = [(UNMARKED, i) for i in range(0, N)]
        stored = list(range(N))
        random.shuffle(stored)
        R2_iterations = run(R2, stored, tree)
        print("  R2 - iterations: {}".format(R2_iterations))

        # Setup for R3.
        tree = [(UNMARKED, i) for i in range(0, N)]
        stored = list(range(N))
        random.shuffle(stored)
        R3_iterations = run(R3(tree), stored, tree)
        print("  R3 - iterations: {}".format(R3_iterations))
        print()

def test_example():
    example_tree = [
        (MARKED, 0),(UNMARKED, 1),(UNMARKED, 2),(MARKED, 3),(UNMARKED, 4),
        (MARKED, 5),(UNMARKED, 6)
    ]

    #Example tree from paper, should complete in one round.
    iterations = run(lambda seed: seed, 4, example_tree)
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
