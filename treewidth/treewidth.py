#!/usr/bin/env python3

import os
import sys
import itertools
import time

FILENAMES =\
"""data/web4
data/WorldMap
data/FibonacciTree_10
data/StarGraph_100
data/TutteGraph
data/DorogovtsevGoltsevMendesGraph
data/HanoiTowerGraph_4_3
data/TaylorTwographDescendantSRG_3
data/CirculantGraph_20_5
data/AhrensSzekeresGeneralizedQuadrangleGraph_3
data/DesarguesGraph
data/FranklinGraph
data/FolkmanGraph
data/GoldnerHararyGraph
data/FriendshipGraph_10
data/HerschelGraph
data/HoltGraph
data/Klein7RegularGraph
data/McGeeGraph
data/TaylorTwographSRG_3
data/WellsGraph
data/SierpinskiGasketGraph_3""".splitlines()

SUFFIX_DECOMP = ".td"
SUFFIX_TREE = ".gr"

visited = set()

class Node():

    def __init__(self,c,b,G):
        self.children = c
        self.bag_vertices = b
        self.table = {}
        self.U = []
        for s in create_combinations(self.bag_vertices):
            if isIndependent(s,G):
                self.U.append(s)

    def print_tree(self):
        for c in self.children:
            c.print_tree()
        print(self.bag_vertices)

    def is_in_table(self,K):
        return str(K) in self.table

    def add_to_table(self,K,V):
        self.table[str(K)] = V

    def get_table_value(self,K):
        return self.table[str(K)]

    def make_table_entry(self, u):
        value = len(u)
        if self.children:
            Vt = self.bag_vertices
            for c in self.children:
                 value += c.get_max(u, Vt)
        self.add_to_table(u, value)

    def Ft(self,u):
        if not self.is_in_table(u):
            self.make_table_entry(u)
        return self.get_table_value(u)

    def get_max(self,u,Vt):
        valid_sets = []
        for ui in self.U:
            if ui.intersection(Vt) == u.intersection(self.bag_vertices):
                valid_sets.append(ui)

        # TODO: Store the set ui which corresponds to the max
        return max([self.Ft(ui) - len(ui.intersection(u)) for ui in valid_sets])


def create_combinations(L):
    combinations = []
    for n in range(len(L) + 1):
        for sset in itertools.combinations(L, n):
            combinations.append(set(sset))
    return combinations

def isIndependent(S,G):
    setList = list(S)
    for i in range(len(setList)):
        for j in range(i+1,len(setList)):
            if isConnected(setList[i],setList[j],G) or isConnected(setList[j],setList[i],G):
                return False
    return True


def isConnected(v1,v2,G):
    return v2 in G[v1]

def algorithm(root):
    if root == None:
        return 1
    return root.get_max(set(),set())

def read_data(filename):

    base_name = filename.rsplit(".", 1)[0]

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
            edge_sets[edge_to].add(edge_from)
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
                bag_edges[edge_to].add(edge_from)
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
        data_decomp = read_decomp(get_data(other_name))

    return data_tree, data_decomp

def fancy_print_data(tree_indices, bag_contents, bag_edges):

    print("Edges: ")
    fmt_edge = "  There is a edge from: {} -> {}"
    for edge_from, edges in enumerate(tree_indices):
        for edge_to in edges:
            print(fmt_edge.format(edge_from+1, edge_to+1))

    print("")
    print("Bag contents: ")
    fmt_content = "  Content of bag #{}: {}"
    for number, contents in enumerate(bag_contents):
        content_string = ','.join([str(n+1) for n in contents])
        print(fmt_content.format(number+1, content_string))

    print("")
    print("Bag edges: ")
    fmt_edge = "  There is a edge from: {} -> {}"
    for edge_from, edges in enumerate(bag_edges):
        for edge_to in edges:
            print(fmt_edge.format(edge_from+1, edge_to+1))


def parse_filename(filename):
    global visited
    visited = set()

    tree_indices, (bag_contents, bag_edges) = read_data(filename)

#    fancy_print_data(tree_indices, bag_contents, bag_edges)
    root = build_tree(tree_indices,bag_contents,bag_edges,0)

#    root.print_tree()

    time_begin = time.time()
    size_max_indep_set = algorithm(root)
    time_end = time.time()
    n = len(tree_indices)
    time_diff = time_end-time_begin

    return size_max_indep_set, n, time_diff

def main(args):

    result_file = "dumped_data.txt"

    usage = "Usage: {} data/any-file-in-data".format(__file__)
    if not args:
        print(usage)
        return

    filename = args[0]

    if os.path.isdir(filename): # Is a directory.

        def get_size_of_instance(filename):
            with open(filename, 'r') as fp:
                data = fp.readlines()
                while data[0].strip().startswith("c"):
                    data.pop(0)
                tokens = data[0].split()
                return int(tokens[3])

        #file_name_list = [os.path.join(filename, name) for name in os.listdir(filename) if name.endswith(SUFFIX_DECOMP)]
        file_name_list = ["{}{}".format(name, SUFFIX_DECOMP) for name in FILENAMES]
        file_name_list = sorted(file_name_list, key=get_size_of_instance)

#        for filename in file_name_list:
#            print(filename)
#            print("w = ",get_size_of_instance(filename))
#        return

        for filename in file_name_list:
            w = get_size_of_instance(filename)
            if w == 0: # Ignore empty data.
                continue
            size_max_indep_set, n, time_diff = parse_filename(filename)
            result = ",".join([str(elem) for elem in [filename, n, w,  size_max_indep_set, time_diff]])
            with open(result_file, 'a') as fp:
                fp.write(result+'\n')

    else: # Single file.
        print(parse_filename(filename))


def build_tree(T,bags,E,current):
    global visited
    children = []
    if current in visited:
        return None
    visited.add(current)
    for child in extract_children(E,current):
        got_node = build_tree(T,bags,E,child)
        if got_node:
            children.append(got_node)
    return Node(children,bags[current],T)

def extract_children(node_edges, node):
    return node_edges[node]


if __name__ == "__main__":
    main(sys.argv[1:])
