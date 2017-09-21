#!/usr/bin/env python3

import sys
import time

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
            matrix = [set() for _ in range(num_nodes)]
            for matrix_row, string in zip(matrix, lines):
                for index, value in enumerate(string.split(' ')):
                    if value.strip() == "1":
                        matrix_row.add(index)
            return [num_nodes, matrix]
    except FileNotFoundError:
        return []

R1 = False
R2 = False

matrix = ""
first_time = time.time()
prev_time = time.time()

adjacent = []

def R_recursive(nodes_left):
    global num_call, matrix, prev_time

    if len(nodes_left) == 0:
        return 0

    current_time = time.time()
    if current_time - prev_time >= 1:
        prev_time = current_time
        print("On recursive call: {}.\r".format(num_call), end="")

    num_call += 1

    def node_with_most_adjacent(matrix):
        max_adjacent = 0
        max_index = 0
        for index in nodes_left:
            nodes_adjacent = len(matrix[index])
            if nodes_adjacent > max_adjacent:
                max_index = index
        return max_index

    for index in nodes_left:

        # Get adjacent and number adjacent.
        adjacent_nodes = matrix[index]
        nodes_adjacent = len(adjacent_nodes)

        # Create nodes_left without index.
        left_without_index = set(nodes_left)
        left_without_index.remove(index)

        # Create nodes_left without index and adjacent.
        left_without_adjacent = set(left_without_index)
        left_without_adjacent -= adjacent_nodes

        if nodes_adjacent == 2 and R2: # R2 - trick.
            u, w = adjacent_nodes
            connected = w in matrix[u]
            if connected:
                return 1 + R_recursive(left_without_index)
            else:
                # Calculate z.
                z_index = len(matrix)-1

                # Get adjacent.
                adjacent_nodes_u = matrix[u]
                adjacent_nodes_w = matrix[w]
                # Remove current index (v).
                adjacent_nodes_u.remove(index)
                adjacent_nodes_w.remove(index)

                # Link it up.
                new_adjacent = set()
                new_adjacent.update(adjacent_nodes_u.union(adjacent_nodes_w))
                for index in new_adjacent:
                    matrix[index].add(z_index)
                # Add adjacency for new z to matrix.
                matrix.append(new_adjacent)

                # Remove u,w, and v from nodes left.
                new_nodes_left = set(left_without_index)
                new_nodes_left.remove(u)
                new_nodes_left.remove(w)

                # Add z to nodes left.
                new_nodes_left.add(z_index)

                return 1 + R_recursive(new_nodes_left)

        elif nodes_adjacent == 1 and R1: # R1 - trick.
            return 1 + R_recursive(left_without_adjacent)
        elif nodes_adjacent == 0: # R0 - trick.
            return 1 + R_recursive(left_without_index)

    max_node = node_with_most_adjacent(matrix)

    without_max = set(nodes_left)
    without_max -= set([max_node])

    without_max_adjacent = set(without_max)
    without_max_adjacent -= matrix[max_node]

    val_without_max_adjacent = R_recursive(without_max_adjacent)
    val_without_max = R_recursive(without_max)

    return max(1+val_without_max_adjacent, val_without_max)

def R():

    nodes_left = set(range(len(matrix)))
    return R_recursive(nodes_left)

def main(args):

    global matrix
    global R1, R2

    fmt_usage = "Usage: [python] {} adjacency_data.in [R1] [R2]"
    if not args:
        error(fmt_usage.format(__file__),usage=True)
        return EXIT_ERROR

    filename = args.pop(0)
    data_tokens = load_data(filename)
    if not data_tokens:
        error("Could not open {}, aborting.".format(filename))
        return EXIT_ERROR

    # Unpack data tokens.
    num_nodes, matrix = data_tokens
    tricks = args[:2]
    for t in tricks:
        if t == "R1":
            R1 = True
        elif t == "R2":
            R2 = True

    print("Status: R1 = {}, R2 = {}".format(R1, R2))
    print("\nResult from R: {}.".format(R()))

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
