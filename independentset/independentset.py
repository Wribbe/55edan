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
            return matrix
    except FileNotFoundError:
        return []

def num_neighbours(adjacency_matrix, G, vertex_id):#if (G[vertex_id])
    available_vertices = [v for v in range(len(G)) if G[v]]
    return sum([1 for v in available_vertices if adjacency_matrix[v][vertex_id]])

def get_neighbours(adjacency_matrix,G,vertex_id):
    available_vertices = [v for v in range(len(G)) if G[v]]
    return [v for v in available_vertices if adjacency_matrix[v][vertex_id]]



def find_max_degree(adjacency_matrix, G):
    # extract vertix ids that are still in G
    available_vertices = [v for v in range(len(G)) if G[v]]
    max_degree_vertex = (0, 0) # (vertex_id, degree)
    for v in available_vertices:
        numN = num_neighbours(adjacency_matrix, G, v)
        if numN > max_degree_vertex[1]:
            max_degree_vertex = (v,numN)
    return max_degree_vertex[0]

def indep_set(adjacency_matrix, G, n):
    if not any(G):
        return 0
    available_vertices = [v for v in range(len(G)) if G[v]]
    #Finding a vertex without neighbours
    for v in available_vertices:
        if num_neighbours(adjacency_matrix,G,v) == 0:
            new_G = list(G)
            new_G[v] = False
            return 1 + indep_set(adjacency_matrix,new_G,n)
    max_vertex = find_max_degree(adjacency_matrix,G)
    new_G = list(G)
    new_G[max_vertex] = False
    new_G2 = list(G)
    for v in get_neightbours:
        new_G2[v] = False
    new_G2[max_vertex] = False
    return max(1 + indep_set(adjacency_matrix,new_G,n),indep_set(adjacency_matrix,new_G2,n))
    
def main(args):

    fmt_usage = "Usage: [python] {} adjacency_data.in"
    if not args:
        error(fmt_usage.format(__file__),usage=True)
        return EXIT_ERROR

    filename = args[0]
    matrix = load_data(filename)
    if not matrix:
        error("Could not open {}, aborting.".format(filename))
        return EXIT_ERROR

    print(matrix)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
