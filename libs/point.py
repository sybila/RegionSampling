class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __str__(self):
        return str(self.position) + ":" + str(self.value)

    def __repr__(self):
        return str(self)

    def projection(self, pos):
        return self.position[pos]

    def check_other_dims(self, dims):
        for dim in dims.keys():
            if self.position[dim] != dims[dim]:
                return False
        return True


def get_bounds_positions(ordered_params, sample_space, x, y):
    return {"x_min": sample_space[ordered_params[x]][0], "x_max": sample_space[ordered_params[x]][-1],
            "y_min": sample_space[ordered_params[y]][0], "y_max": sample_space[ordered_params[y]][-1]}


def get_bounds_values(points):
    values = [point.value for point in points]
    return min(values), max(values)


def filter_points(points, dims):
    return list(filter(lambda point: point.check_other_dims(dims), points))
