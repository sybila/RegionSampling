import argparse
import sys, os
import numpy as np
import itertools

# this add to path RegionSampling home dir, so it can be called from anywhere
sys.path.append(os.path.split(sys.path[0])[0])

from libs.point import get_bounds_positions, get_bounds_values, filter_points
from libs.parsing import parse_storm_file
from libs.sampling import samplePoints
from libs.svg import Picture
import libs.html


def sample(storm_file, params):
    output = ""
    function = parse_storm_file(storm_file)

    sample_space = {key: np.linspace(params[key][0], params[key][1], params[key][2])
                    for key in params}

    ordered_params = list(sample_space.keys())

    points = samplePoints(function, sample_space, ordered_params)
    min_val, max_val = get_bounds_values(points)
    indices = set(range(len(ordered_params)))

    if len(ordered_params) <= 2:
        output += (libs.html.HTML_start_2d)
    else:
        output += (libs.html.HTML_start_more_d_1)
        output += ("\t\t\tvar dims = {}\n".format(["dim_{}".format(i) for i in range(len(ordered_params) - 2)]))
        output += ("\t\t\tvar params = {}\n".format(ordered_params))
        for param in sample_space:
            output += ("\t\t\tvar {} = {}\n".format(param, list(sample_space[param])))
        output += (libs.html.HTML_start_more_d_2)
        output += ("\t\t\tvar dims = {}".format(["dim_{}".format(i) for i in range(len(ordered_params) - 2)]))
        output += (libs.html.HTML_start_more_d_3)

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

                dims_values = {key: other_dims[key][dims[key]] for key in dims}

                filtered_points = filter_points(points, dims_values)

                pic = Picture(bounds_pos, False)
                pic.load_points(filtered_points, x, y, min_val, max_val)

                dims_label = "_".join([ordered_params[param] + "_" + str(dims[param]) for param in dims])

                output += ('\t\t\tvar {}_{}_{} = "data:image/svg+xml;utf8,{}"\n'.format(ordered_params[x],
                                                                                     ordered_params[y],
                                                                                     dims_label, pic))
        else:
            pic = Picture(bounds_pos, False)
            pic.load_points(points, x, y, min_val, max_val)
            output += ('\t\t\tvar {}_{} = "data:image/svg+xml;utf8,{}"\n'.format(ordered_params[x],
                                                                              ordered_params[y], pic))

    # print mid
    output += (libs.html.HTML_mid)
    output += (libs.html.HTML_x_axis)

    # print x-axis options
    output += (libs.html.print_option(ordered_params[0], True))
    for param in ordered_params[1:]:
        output += (libs.html.print_option(param))

    output += (libs.html.HTML_y_axis)
    output += (libs.html.print_option(ordered_params[0]))
    output += (libs.html.print_option(ordered_params[1], True))
    for param in ordered_params[2:]:
        output += (libs.html.print_option(param))

    # print end
    output += (libs.html.HTML_end_1)

    # print other dimensions
    if len(ordered_params) > 2:
        output += (libs.html.HTML_other_dim)
        for i in range(len(ordered_params) - 2):
            output += (libs.html.HTML_dim_options.format(i, ordered_params[i+2]))
            values = sample_space[ordered_params[i+2]]
            for j in range(len(values)):
                output += (libs.html.print_fixed_option(j, values[j]))
            output += (libs.html.HTML_dim_options_end)

    # print end
    output += (libs.html.HTML_end_2)
    return output


'''
usage: run.py [-h] --storm_file STORM_FILE --output OUTPUT --params PARAMS

Region sampling

arguments:
  -h, --help            show this help message and exit
  --storm_file STORM_FILE
  --output OUTPUT
  --params PARAMS


Example:
    python3 run.py storm_output.txt '{"q" : [5, 10, 10], "p" : [0, 2, 10]}' output.html
'''


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='Region sampling')
    args_parser.add_argument('--storm_file', type=str, required=True)
    args_parser.add_argument('--output', type=str, required=True)
    args_parser.add_argument('--params', required=True)

    args = args_parser.parse_args()

    params = eval(args.params)
    
    out = sample(args.storm_file, params)

    f = open(args.output, "w")
    f.write(out)
    f.close()
    