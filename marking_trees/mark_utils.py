import sys
import json

KEY_HEADING = 'heading'
KEY_ITERATIONS = 'iterations'

KEY_R1 = "R1"
KEY_R2 = "R2"
KEY_R3 = "R3"

NO_OUTPUT = False

def our_print(text="", **kwargs):
    if NO_OUTPUT:
        return
    print(text, **kwargs)

def dump_json(data):
    """ Assemble dict data in data list and print to standard out. """
    json_dict = {}
    # Iterate over all current dictionaries in data.
    for dictionary in data:
        _, N = dictionary.get(KEY_HEADING)
        # Make sure a dictionary for current N exists.
        Ndict = json_dict.get(N)
        if not Ndict:
            Ndict = json_dict[N] = {}
        # Iterate over all 'choice-functions'.
        for Rx in [KEY_R1, KEY_R2, KEY_R3]:
            # Make sure there exists a list to store iteration values.
            Rlist = Ndict.get(Rx)
            if not Rlist:
                Rlist = Ndict[Rx] = []
            # Get number of iterations for Rx.
            _, iterations = dictionary[KEY_ITERATIONS][Rx]
            # Append the number of iterations to the correct list.
            Rlist.append(iterations)
    # Create pretty printed JSON output.
    json_string = json.dumps(json_dict, sort_keys=True, indent=4,
            separators=(',', ': '))
    return json_string

def add_to_dict(dictionary, keys, value, last=False):

    output_formats = {
        KEY_HEADING : "h={}, N={}",
        KEY_ITERATIONS: "{} - iterations: {}",
    }

    def output_printer(fmt_text, values, last):
        """ Print information about finished markings to stdout. """
        # Ensure that values are wrapped in a list to enable expansion.
        if not type(values) == list:
            values = [values]
        our_print(fmt_text.format(*values))
        if last: # Additional spacing after last entry.
            our_print()

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

