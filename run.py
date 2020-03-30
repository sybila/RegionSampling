import sys
import numpy as np
import itertools

from libs.point import get_bounds_positions, get_bounds_values, filter_points
from libs.parsing import parse_storm_file
from libs.sampling import samplePoints
from libs.svg import Picture

'''
python3 sample.py <storm_output_file> <parameter_intervals> <output_html_file>

where <parameters> is a dictionary of type:
    "param-name" : [from, to, number]
    which will create a linear space
    with interval (<from>, <to>) and <number> samples.

Example:
    python3 sample.py storm_output.txt '{"q" : [5, 10, 10], "p" : [0, 2, 10]}' output.html
'''
if __name__ == '__main__':
    output_file = sys.argv[-1]
    params = eval(sys.argv[-2])
    storm_file = sys.argv[-3]

    function = parse_storm_file(storm_file)

    sample_space = {key: np.linspace(params[key][0], params[key][1], params[key][2])
                    for key in params}

    ordered_params = list(sample_space.keys())

    points = samplePoints(function, sample_space, ordered_params)
    min_val, max_val = get_bounds_values(points)
    indices = set(range(len(ordered_params)))

    for (x, y) in itertools.permutations(indices, 2):
        bounds_pos = get_bounds_positions(ordered_params, sample_space, x, y)

        # extract all other dimensions
        other_dims = {i: sample_space[ordered_params[i]] for i in indices - {x, y}}
        if other_dims:
            position_dims = {key: list(range(len(other_dims[key]))) for key in other_dims.keys()}
            # used to obtain particular index from combinations
            ordered_other_dims = list(other_dims.keys())

            # combinations of all positions of all params
            combinations = itertools.product(*(position_dims[name] for name in ordered_other_dims))
            # values correspond to param names in ordered_names
            for combination in combinations:
                dims = dict(zip(ordered_other_dims, combination))

                filtered_points = filter_points(points, dims)
                print(x, y, dims, len(filtered_points))

                pic = Picture(bounds_pos)
                pic.load_points(filtered_points, x, y, min_val, max_val, bounds_pos)
                # print(pic)

    # probs = column(points, 2)
    #
    # bounds = {"w_min": params[keys[0]][0], "w_max": params[keys[0]][1],
    #           "h_min": params[keys[1]][0], "h_max": params[keys[1]][1]}
    #
    #
    # pic.load_points(points, min(probs), max(probs), bounds)
    # pic.save(output_file)
