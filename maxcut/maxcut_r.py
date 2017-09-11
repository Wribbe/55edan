#!/usr/bin/env python3

import sys
import os
import regex

def make_graph(n, m, edges):
    # vertex format := (edge-count, [ (dest, weight)* ])
    vertex = [(0, []) for i in range(0, n)]
    for edge in edges:
        src, dest, weight = edge[0], edge[1], edge[2]
        print("vertex=" + str(src) + " edge=" + "(" + str(dest) + "," + str(weight) + ")")

        new_edge_count = vertex[src][0] + 1

        new_edge_list = vertex[src][1]
        new_edge_list.append((dest, weight))

        vertex[src] = (new_edge_count, new_edge_list)
    return vertex

def load_graph(folder, filename):
    load_path = os.path.join(folder, filename)

    if filename in os.listdir(folder):
        print("Loading graph from path=" + load_path)
        text = open(load_path, mode='r').read()
        text = regex.sub(r'\s+', r' ', text)
        data = text.split()
        n, m, edges = data[0], data[1], data[2:]

        # remap edge labels to [0, n-1]
        edges = [int(i)-1 for i in edges]

        # extract edge triples (src, dest, weight)
        edges = [edges[i*3 : 3*(i+1)] for i in (range(0, int(len(edges) / 3)))]

        return make_graph(int(n), int(m), edges)
    else:
        print("Unable to open file.")
        sys.exit(1)

def main(filename):
    folder = "." + os.path.sep
    load_graph(folder, filename)

if __name__ == '__main__':
    main(sys.argv[1])
