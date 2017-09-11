#!/usr/bin/env python3

import sys

EXIT_ERROR = -1

def print_graph(vertices):
    # {x} specifies the x'th input to be used by format.
    # "{0}-{0}-{1}".format('a','b') -> "a-a-b".
    format_vertex = "vertex={0} edge={0}--{1}, w={2}"
    for index, edge_list in enumerate(vertices, start=1):
        for destination, weight in edge_list:
            # Restore destination from 0..n-1 -> 1..n.
            destination += 1
            print(format_vertex.format(index, destination, weight))

def main(args):

    usage = "[python] {} input_file.txt [--print-tree]"
    if not args:
        print(usage.format(__file__))
        return EXIT_ERROR

    filename = args[0]
    vertices = []

    try:
        with open(filename, 'r') as fp:
            lines = [line.strip() for line in fp.readlines()]
            # Parse heading and create vertices structure.
            heading = lines.pop(0)
            num_vertices, num_edges = [int(num) for num in heading.split()]
            # Can't use [[]]*num pattern, all inner lists points to same list.
            # Adding an element to one adds it to all lists, weird..
            vertices = [[] for _ in range(num_vertices)]
            # Iterate over all data-lines.
            for line in lines:
                numbers = [int(x) for x in line.split()]
                # Unpack numbers read from line.
                index, destination, weight = numbers
                # Move index and destination from 1..n to 0..n-1.
                index -= 1
                destination -= 1
                # Add edge to correct index.
                vertices[index].append((destination, weight))
    except FileNotFoundError as e:
        print("Could not open '{}', aborting.".format(filename),
              file=sys.stderr)
        return EXIT_ERROR

    if '--print-tree' in args:
        print_graph(vertices)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
