#!/usr/bin/env python3

import math
import random
import sys

MARKED = 'm'
UNMARKED = 'u'

INFO_OUTPUT = True
OUTPUT_JSON = False

def sibling(index):
    if index%2 == 0:
        return index-1
    return index+1

def parent(index):
    half_index = int(index/2)
    if index%2 == 0:
        return half_index-1
    return half_index

def children(index):
    left_child = (index*2)+1
    right_child = left_child+1
    return [left_child, right_child]

def has_children(index, tree):
    return [i for i in children(index) if i < len(tree)]

def marked(index, tree):
    return tree[index] == MARKED

def mark(index, tree):
    """ Apply marking rules and return nodes that should be marked in the
    future.

    Rules:
        - If parent and sibling to a node is marked, mark node.
        - If both children to node are marked, mark node.
    """
    to_be_marked = []
    tree[index] = MARKED

    if has_children(index, tree):

        child_left, child_right = children(index)

        marked_left = marked(child_left, tree)
        marked_right = marked(child_right, tree)

        if marked_left and not marked_right:
            to_be_marked.append(child_right)
        elif marked_right and not marked_left:
            to_be_marked.append(child_left)

    if index > 0: # Not in root node.

        index_parent = parent(index)
        index_sibling = sibling(index)

        marked_parent = marked(index_parent, tree)
        marked_sibling = marked(index_sibling, tree)

        if not marked_parent and marked_sibling:
            to_be_marked.append(index_parent)
        elif not marked_sibling and marked_parent:
            to_be_marked.append(index_sibling)

    return to_be_marked

def mark_tree(value, tree):
    mark_queue = [value] if not marked(value, tree) else []
    n_marked = 0

    while mark_queue:
        index_to_mark = mark_queue.pop(0)
        if marked(index_to_mark, tree):
            continue
        mark_queue += mark(index_to_mark, tree)
        n_marked += 1
    return n_marked

def R1(N, start=0):
    return random.randint(start,N-1)

def R2(stored):
    return stored.pop()

def R3(stored, tree):
    index = stored.pop()
    while marked(index, tree):
        index = stored.pop()
    return index

def print_info(iterations, erase=False):
    if not INFO_OUTPUT:
        return

    def rewriting_print(text):
        """ Re-/over-writing print method to standard error output without
        added newline.
        """
        print("{}\r".format(text), end="", file=sys.stderr)

    format_info = "INFO -- current iteration: {}"
    info_line = format_info.format(iterations)

    if erase:
        # Make sure all previously written characters are replaced with spaces.
        info_line = ' '*len(info_line)
    rewriting_print(info_line)

def run(index_generator, generator_input, tree):
    iterations = 0
    n_marked = len([node for node in tree if node == MARKED])
    while n_marked != len(tree):
        iterations += 1
        # The pattern `function(*[list, of, vars])` is equal to the following
        # call:
        #   function(list, of, vars)
        next_index = index_generator(*generator_input)
        n_marked += mark_tree(next_index, tree)
        print_info(iterations)
    print_info(iterations, erase=True)
    return iterations

def main():

    h_max = 20
    h_start = 2
    data = []

    KEY_HEADING = 'heading'
    KEY_ITERATIONS = 'iterations'

    KEY_R1 = "R1"
    KEY_R2 = "R2"
    KEY_R3 = "R3"

    def add_to_dict(dictionary, keys, value, last=False):

        output_formats = {
            KEY_HEADING : "h={}, N={}",
            KEY_ITERATIONS: "{} - iterations: {}",
        }

        def output_printer(fmt_text, values, last):
            """ Print to standard out or standard error depending on JSON
            output.
            """

            # Ensure that values are wrapped in a list to enable expansion.
            if not type(values) == list:
                values = [values]

            output_stream = sys.stdout
            if OUTPUT_JSON:
                output_stream = sys.stderr
            print(fmt_text.format(*values), file=output_stream)
            if last: # Additional spacing after last entry.
                print()

        # Make sure that it's possible to iterate over provided keys.
        if not type(keys) == list:
            keys = [keys]

        def make_sure_dict_exists(dictionary, key):
            """ Make sure that there is a dictionary corresponding to the given
            key, if there is none, create it.
            """
            exists = dictionary.get(key)
            if not exists:
                exists = dictionary[key] = {}
            return exists

        # Retrieve main dictionary key, and corresponding data.
        main_key = keys[0]
        make_sure_dict_exists(dictionary, main_key)

        # The final value should be at current_dict[last_key].
        current_dict = dictionary
        last_key = main_key
        if keys:
            last_key = keys.pop(-1)
        for key in keys: # Build rest of intermediate dictionary structure.
            current_dict = make_sure_dict_exists(current_dict, key)

        # At bottom of existing or created dictionary structure, add value.
        current_dict[last_key] = value
        # Print output with predefined formatting.
        output_printer(output_formats[main_key], value, last)

    for h in range(h_start,h_max+1):

        # Create and append data dictionary.
        dict_data = {}
        data.append(dict_data)

        # Setup and add heading to dict.
        N = int(math.pow(2,h)-1)
        add_to_dict(dict_data, KEY_HEADING, [h, N])

        # Setup for R1.
        tree = [UNMARKED] * N
        R1_iterations = run(R1, [N], tree)
        add_to_dict(dict_data, [KEY_ITERATIONS, KEY_R1], ["R1", R1_iterations])

        # Setup for R2.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R2_iterations = run(R2, [stored], tree)
        add_to_dict(dict_data, [KEY_ITERATIONS, KEY_R2], ["R2", R2_iterations])

        # Setup for R3.
        tree = [UNMARKED] * N
        stored = list(range(N))
        random.shuffle(stored)
        R3_iterations = run(R3, [stored, tree], tree)
        add_to_dict(dict_data, [KEY_ITERATIONS, KEY_R3], ["R3", R3_iterations],
                last=True)

def test_tree_passes():
    # Example tree from paper, should complete in one round.
    example_tree = [
            MARKED, UNMARKED, UNMARKED, MARKED, UNMARKED, MARKED, UNMARKED
            ]

    # Make sure that R1 picks a value between 4 and 5-1 --> 4.
    R1start = 4
    R1stop = 5
    iterations = run(R1, [R1stop,R1start], example_tree)
    return iterations == 1

if __name__ == "__main__":

    # Parse command line arguments.
    args = sys.argv[1:]
    if '--no-info' in args:
        INFO_OUTPUT = False
    if '--json' in args:
        OUTPUT_JSON = True

    # Test if test tree passes, otherwise abort.
    if not test_tree_passes():
        print("Example tree should complete in one iteration " +\
              "with R1 and input-index 4, aborting. ")
        sys.exit(-1)

    # Test passed, run main method.
    main()
