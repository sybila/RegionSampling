def parse_storm_file(filename):
    input_file = open(filename, "r")
    function = ""
    for line in input_file.readlines():
        if line.rstrip():
            if "Result (initial states):" in line:
                function = line.split(":")[1]
                break
    if not function:
        raise Exception("No function found.")
    return function
