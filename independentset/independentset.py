#!/usr/bin/env python3

import sys

EXIT_ERROR = -1

num_call = 0

def error(message="", usage=False, **kwargs):
    error_prefix = "[!] - "
    if usage:
        error_prefix = ""
    print("{}{}".format(error_prefix, message, file=sys.stderr, **kwargs))

def load_data(filename):
    try:
        with open(filename, 'r') as fp:
            lines = [line.strip() for line in fp.readlines()]
            num_nodes = int(lines.pop(0))
            matrix = [[] for _ in range(num_nodes)]
            for matrix_row, string in zip(matrix, lines):
                matrix_row += [int(value) == 1 for value in string.split(' ')]
            return [num_nodes, matrix]
    except FileNotFoundError:
        return []

def available_vertices(G):
    return [index for index, _ in enumerate(G) if G[index]]

def neighbours(adjacency_matrix,G,vertex_id):

    def edge_exists(index1, index2):
        return adjacency_matrix[index1][index2]

    available = available_vertices(G)
    return [index for index in available if edge_exists(index, vertex_id)]

def find_max_degree(adjacency_matrix, G):
    # Extract vertex ids that are still in G.
    available_vertices = [v for v in range(len(G)) if G[v]]
    max_degree_vertex = (0, 0) # (vertex_id, degree)
    for v in available_vertices:
        numN = len(neighbours(adjacency_matrix, G, v))
        if numN > max_degree_vertex[1]:
            max_degree_vertex = (v,numN)
    return max_degree_vertex[0]

def myR1_recursive(matrix, nodes_left):

    global num_call
    print("On recursive call: {}\r".format(num_call), end="")
    num_call += 1

    def adjacent(index):
        adjacent_nodes = []
        row = matrix[index]
        for left_index, left in enumerate(nodes_left):
            if left and row[left_index]:
                adjacent_nodes.append(left_index)
        return adjacent_nodes

    def num_adjacent(index):
        return int(len(adjacent(index)))

    def node_with_most_adjacent(matrix):
        max_adjacent = 0
        max_index = 0
        for index, left in enumerate(nodes_left):
            if not left:
                continue
            nodes_ajdacent = num_adjacent(index)
            if nodes_ajdacent > max_adjacent:
                max_index = index
        return max_index

    def remove_index(index):
        copy = list(nodes_left)
        copy[index] = False
        return copy

    def remove_index_and_adjacent(index):
        copy = remove_index(index)
        for index_node in adjacent(index):
            copy[index_node] = False
        return copy

    if not any(nodes_left):
        return 0

    for index, valid in enumerate(nodes_left):
        if not valid:
            continue
        if num_adjacent(index) == 0:
            return 1 + myR1_recursive(matrix, remove_index(index))

    max_node = node_with_most_adjacent(matrix)

    without_max_and_adjacent = remove_index_and_adjacent(max_node)
    without_max = remove_index(max_node)

    val_without_max_adjacent = myR1_recursive(matrix, without_max_and_adjacent)
    val_without_max = myR1_recursive(matrix, without_max)

    return max(1+val_without_max_adjacent, val_without_max)


def myR1(matrix):

    nodes_left = [True] * len(matrix)
    return myR1_recursive(matrix, nodes_left)

def R1(adjacency_matrix, G, n):

    # If nodes available, end recursion.
    # If the graph (G?) is empty, end recursion.
    if not any(G):
        return 0

    # Find any vertex that has 0 pals.
    for v in available_vertices(G):
        if len(neighbours(adjacency_matrix,G,v)) == 0:
            #print("Found a vertice with no pals.", v)
            new_G = list(G)
            new_G[v] = False
            return 1 + R1(adjacency_matrix,new_G,n)

    # If there were no 0-pal verticies, find the one with maximum pals.
    max_vertex = find_max_degree(adjacency_matrix,G)
    #print("max_vertex", max_vertex)
    new_G = list(G)
    new_G[max_vertex] = False
    new_G2 = list(G)

    # Iterate over all max-pal pals and remove them from new G.
    for v in neighbours(adjacency_matrix, G, max_vertex):
        #print(neighbours(adjacency_matrix, G, max_vertex))
        new_G2[v] = False
    new_G2[max_vertex] = False

    value_of_R1_max_vertex_removed = R1(adjacency_matrix,new_G,n)
    value_of_R1_max_and_pals_removed = 1 + R1(adjacency_matrix,new_G2,n)

    return max(value_of_R1_max_vertex_removed,
            value_of_R1_max_and_pals_removed)

def main(args):

    fmt_usage = "Usage: [python] {} adjacency_data.in"
    if not args:
        error(fmt_usage.format(__file__),usage=True)
        return EXIT_ERROR

    filename = args[0]
    data_tokens = load_data(filename)
    if not data_tokens:
        error("Could not open {}, aborting.".format(filename))
        return EXIT_ERROR

    # Unpack data tokens.
    num_nodes, matrix = data_tokens
#
#    G = [True] * num_nodes
#    result = R1(matrix, G, num_nodes)

    print("\nResult from myR1: {}".format(myR1(matrix)))

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
