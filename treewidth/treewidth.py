#!/usr/bin/env python3

import os
import sys

SUFFIX_DECOMP = ".td"
SUFFIX_TREE = ".gr"

class Node():

    def __init__(self):
        self.children = []

    def add(child):
        self.children.append(child)

def read_data(filename):

    base_name = filename.split(".")[0]

    def is_comment(line):
        if line.strip().startswith('c'):
            return True
        return False

    def get_data(filename):
        data = ""
        with open(filename, 'r') as fp:
            data = fp.readlines()
            # Remove all leading comments.
            while is_comment(data[0]):
                data.pop(0)
        return data

    def read_tree(data):
        p_line = data.pop(0)
        # Throw away the fist 2 tokens.
        num_vertices, num_edges = [int(n) for n in p_line.strip().split()[2:]]
        edge_sets = [set() for _ in range(num_vertices)]
        for line in data:
            if is_comment(line):
                continue
            # Move index range from 1..n to 0..n-1.
            edge_from, edge_to = [int(n)-1 for n in line.strip().split()]
            edge_sets[edge_from].add(edge_to)
        return edge_sets

    def read_decomp(data):
        s_line = data.pop(0)
        # Throw away the fist 2 tokens.
        num_bags, width, num_vertices = [int(n) for n in s_line.split()[2:]]
        bag_contents = [set() for _ in range(num_bags)]
        bag_edges = [set() for _ in range(num_bags)]
        for line in data:
            if is_comment(line):
                continue
            if line.startswith('b'): # Bag content line.
                tokens = line.strip().split()
                # Throw away the 'b' prefix.
                tokens.pop(0)
                # Move index ranges from 1..n to 0..n-1.
                tokens = [int(n)-1 for n in tokens]
                bag_number = tokens.pop(0)
                # Use union operator '|=' to add contents.
                bag_contents[bag_number] |= set(tokens)
            else: # Bag edge line.
                # Move index ranges from 1..n to 0..n-1.
                edge_from, edge_to = [int(n)-1 for n in line.split()]
                bag_edges[edge_from].add(edge_to)
        return bag_contents, bag_edges

    data_tree = ""
    data_decomp = ""

    if filename.endswith(SUFFIX_DECOMP):
        data_decomp = read_decomp(get_data(filename))
        other_name = "{}{}".format(base_name, SUFFIX_TREE)
        data_tree = read_tree(get_data(other_name))
    else:
        data_tree = read_tree(get_data(filename))
        other_name = "{}{}".format(base_name, SUFFIX_DECOMP)
        data_decomp = read_tree(get_data(other_name))

    return data_tree, data_decomp

def main(args):

    usage = "Usage: {} data/any-file-in-data".format(__file__)
    if not args:
        print(usage)
        return

    filename = args[0]
    tree_indices, (bag_contents, bag_edges) = read_data(filename)
    print("tree indices: {}.".format(tree_indices))
    print("bag contents: {}.".format(bag_contents))
    print("bag edges: {}.".format(bag_edges))

if __name__ == "__main__":
    main(sys.argv[1:])
