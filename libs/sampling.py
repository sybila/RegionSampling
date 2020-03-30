from sympy import Symbol, zoo
from sympy.parsing.sympy_parser import parse_expr
import itertools

from libs.point import Point


def samplePoints(function, sample_space, ordered_params):
    for param in sample_space.keys():
        exec("{0} = Symbol('{0}')".format(param))

    combinations = itertools.product(*(sample_space[param] for param in ordered_params))

    symbols = []
    for symbol in ordered_params:
        symbols.append(eval(symbol))

    function = parse_expr(function)
    results = []

    for values in combinations:
        result = function.subs(dict(zip(symbols, values)))
        if not result == zoo:
            results.append(Point(values, result))

    return results
