#!/usr/bin/env python3

import sys

EXIT_ERROR = -1

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

    G = [True] * num_nodes
    result = R1(matrix, G, num_nodes)
    print("Result from R1:", result)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
