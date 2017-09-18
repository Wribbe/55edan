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
            lines = fp.readlines()
            num_nodes = int(lines.pop(0))
            matrix = [[] for _ in range(num_nodes)]
            for matrix_row, string in zip(matrix, lines):
                matrix_row += [int(value) == 1 for value in string.split(' ')]
            return matrix
    except FileNotFoundError:
        return []

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
