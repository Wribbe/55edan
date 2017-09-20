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

def myR1_recursive(matrix, nodes_left):

    global num_call
    print("On recursive call: {}\r".format(num_call), end="")
    num_call += 1

    def adjacent(index):
        adjacent_nodes = []
        row = matrix[index]
        for node_index, left in enumerate(nodes_left):
            if left and row[node_index]:
                adjacent_nodes.append(node_index)
        return adjacent_nodes

    def num_adjacent(index):
        return int(len(adjacent(index)))

    def node_with_most_adjacent(matrix):
        max_adjacent = 0
        max_index = 0
        for index, left in enumerate(nodes_left):
            if not left:
                continue
            nodes_adjacent = num_adjacent(index)
            if nodes_adjacent > max_adjacent:
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

    for index, valid in enumerate(list(nodes_left)):
        if not valid:
            continue

        adjacent_nodes = adjacent(index)
        nodes_adjacent = len(adjacent_nodes)

        if nodes_adjacent == 2: # R2 - trick.
            u, w = adjacent_nodes
            connected = matrix[u][w]
            if connected:
                return 1 + myR1_recursive(matrix,
                        remove_index_and_adjacent(index))
            else:
                # Add z.
                matrix_copy = [list(row)+[False] for row in matrix]
                z_index = len(matrix_copy[0])-1
                matrix_copy += [[False] * (z_index + 1)]
                # Get adjacent.
                adjacent_nodes_u = adjacent(u)
                adjacent_nodes_w = adjacent(w)
                # Remove current index (v).
                adjacent_nodes_u.remove(index)
                adjacent_nodes_w.remove(index)
                # Link it up.
                for node_index in adjacent_nodes_u + adjacent_nodes_w:
                    matrix_copy[z_index][node_index] = True
                    matrix_copy[node_index][z_index] = True
                # Add z to nodes left.
                new_nodes_left = remove_index_and_adjacent(index)
                new_nodes_left.append(True)
                return 1 + myR1_recursive(matrix_copy, new_nodes_left)

        elif nodes_adjacent == 1: # R1 - trick.
            return 1 + myR1_recursive(matrix, remove_index_and_adjacent(index))
        elif nodes_adjacent == 0: # R0 - trick.
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
