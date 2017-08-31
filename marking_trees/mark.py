#!/usr/bin/env python3

import math
import random

MARKED = 'm'
UNMARKED = 'u'

R2_indexes = []
R3_indexes = []

num_marked = 0
global_N = 0

def main():
    start_h = 2
    max_h = 20

    def new_tree(N):
        global global_N
        global num_marked
        global_N = N
        num_marked = 0
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
        global num_marked
        if marked(index):
            return
        tree[index] = MARKED;
        num_marked += 1

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
            if index < 0 or index > global_N-1 or visited[index]:
                return
            if not marked(index):
                if marked(children(index)) or \
                   marked([parent(index), sibling(index)]):
                    print("executed rule..")
                    mark(index)
            visited[index] = True
            execute_rule(parent(index)) # Continue upwards.
            execute_rule(children(index)) # Continue downwards.

    def all_marked():
        return num_marked == global_N

    def R1(N):
        index = random.randint(0,N-1)
        mark(index)
        return index

    def R2(N):
        global R2_indexes
        if not R2_indexes:
            R2_indexes = list(range(N))
            random.shuffle(R2_indexes)
        index = R2_indexes.pop()
        mark(index)
        return index

    def R3(N):
        global R3_indexes
        if not R3_indexes:
            R3_indexes = list(range(N))
            random.shuffle(R3_indexes)
        index = R3_indexes.pop()
        while marked(index): # Throw away already marked indexes.
            index = R3_indexes.pop()
        mark(index)
        return index

    def run_untill_marked(N, marking_function):
        global tree
        global visited
        visited, tree = new_tree(N)
        rounds = 0
        while not all_marked():
            index = marking_function(N)
            vistited = [False] * global_N
            execute_rule(index)
            rounds += 1
        return rounds

    for h in range(start_h, max_h+1):

        N = int(math.pow(2, h)-1)

        rounds = [run_untill_marked(N, method) for method in [R1,R2,R3]]

        print("N={}, h={}:".format(N, h))
        for index, num_rounds in enumerate(rounds, start=1):
            print("  R{} = {}".format(index, num_rounds))

if __name__ == "__main__":
    main()
