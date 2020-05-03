# RegionSampling
Sampling of parameter function.

Visualisation of quantitative model checking using a sampling of rational function. It samples given parameter space with a given precision and creates a visualisation where colour is assigned to each value.

Usage:
```
python3 run.py <storm_output_file> <parameter_intervals> <output_html_file>

where <parameters> is a dictionary of type:
    "param-name" : [from, to, number]
    which will create a linear space
    with interval (<from>, <to>) and <number> samples.

Example:
    python3 run.py storm_output.txt '{"q" : [5, 10, 10], "p" : [0, 2, 10]}' output.html
```
