#!/usr/bin/env python3

import sys
import random

EXIT_ERROR = -1

def R(vertices):
    A = set()
    for index in range(len(vertices)):
        if random.choice([True, False]) == True:
            A.add(index)
    return A

def print_data(vertices):
    # {x} specifies the x'th input to be used by format.
    # "{0}-{0}-{1}".format('a','b') -> "a-a-b".
    format_vertex = "vertex={0} edge={0}--{1}, w={2}"
    for index, edge_list in enumerate(vertices, start=1):
        for destination, weight in edge_list:
            # Restore destination from 0..n-1 -> 1..n.
            destination += 1
            print(format_vertex.format(index, destination, weight))

def load_data(filename):
    vertices = []
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
            # Add same edge to to destination index.
            vertices[destination].append((index, weight))
    return vertices

def calculate_maxcut_with(vertices, subset_method):

    def c(subset_A, vertices):
        cutting_sum = 0
        for index in subset_A:
            for destination, weight in vertices[index]:
                if destination not in subset_A:
                    cutting_sum += weight
        return cutting_sum

    subset_A = subset_method(vertices)
    return c(subset_A, vertices)

def main(args):

    usage = "[python] {} input_file.txt iterations [--print-data]"
    if len(args) < 2 :
        print(usage.format(__file__))
        return EXIT_ERROR

    filename, iterations = args
    iterations = int(iterations)

    try:
        vertices = load_data(filename)
    except FileNotFoundError as e:
        fmt_error = "Could not open '{}', aborting."
        print(fmt_error.format(filename), file=sys.stderr)
        return EXIT_ERROR

    if '--print-data' in args:
        print_data(vertices)

    cut_sum_list = []
    for _ in range(iterations):
        cut_sum_list.append(calculate_maxcut_with(vertices, R))
    print(cut_sum_list)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
