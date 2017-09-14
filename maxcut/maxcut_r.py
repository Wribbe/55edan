#!/usr/bin/env python3

import sys
import random

EXIT_ERROR = -1

def R(vertices):
    """ Partition vertices based on coin toss. """
    coin = lambda : random.choice([True,False])
    return [i for i, _ in enumerate(vertices) if coin()]

def S(vertices):
    """ All vertices start outside of A.
        - Vertices can be swapped from A <-> !A.
        - Goal to increase cut.
        - Continue until there is no swap that increases the size of the cut.
    """

    inside_a = True
    outside_a = False
    current_cut = 0

    vertice_states = [outside_a] * len(vertices)

    def cut_value_if_swapped(index):
        swapped_state = not vertice_states[index]
        swap_cut = current_cut
        for destination, _ in vertices[index]:
            if swapped_state != vertice_states[destination]:
                swap_cut += 1
            else:
                swap_cut -= 1
        return swap_cut

    def swap(index):
        vertice_states[index] = not vertice_states[index]

    while(True):
        prev_cut = current_cut
        for index, _ in enumerate(vertices):
            swap_cut = cut_value_if_swapped(index)
            if swap_cut > current_cut:
                swap(index)
                current_cut = swap_cut
        if prev_cut == current_cut:
            break # No change after full iteration.

    in_a = lambda index : vertice_states[index]
    return [i for i, _ in enumerate(vertice_states) if in_a(i)]


def calculate_weight(subset, vertices):
    """ Calculate total weight for subset cut. """
    total_weight = 0
    for vertice in vertices:
        total_weight += sum([int(weight) for dest,weight in vertice if dest not
            in subset])
    return total_weight


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

    A = S(vertices)

    #cutset, weight_sum = algorithm_r(vertices, iterations)

    #print("weight_sum=" + str(weight_sum))
    #print("set=" + str(cutset))

    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
