import numpy as np


GRADIENT = \
''' <linearGradient id='gradient'>\
 <stop offset='0%'  stop-color='rgb(255, 0, 0)' />\
 <stop offset='50%'  stop-color='rgb(255,255,0)' />\
 <stop offset='100%' stop-color='rgb(0, 128, 0)' />\
 </linearGradient> \
'''


class Picture():
    def __init__(self, bounds):
        self.regions = []
        self.width_bounds = {'min': 100, 'max': 600}
        self.width_bounds['len'] = self.width_bounds['max'] - self.width_bounds['min']
        self.height_bounds = {'min': 100, 'max': 600}
        self.height_bounds['len'] = self.height_bounds['max'] - self.height_bounds['min']
        self.header = "<svg width='{0}' height='{1}' xmlns='http://www.w3.org/2000/svg'>".format(
            self.width_bounds['max'] + 20, self.height_bounds['max'] + 100)
        self.footer = '</svg>'
        self.lines = []
        self.texts = []
        self.points = []
        self.regions = []
        self.bounds = bounds
        self.axis_description()

    def __str__(self):
        output = self.header
        output += GRADIENT
        for point in self.points:
            output += point + ' '
        for region in self.regions:
            output += region + ' '
        for line in self.lines:
            output += line + ' '
        for text in self.texts:
            output += text + ' '
        output += self.footer
        return output

    def axis_description(self):
        x_axis = np.linspace(self.bounds['x_min'], self.bounds['x_max'], 11)
        y_axis = np.linspace(self.bounds['y_min'], self.bounds['y_max'], 11)

        self.add_line(self.width_bounds['min'], self.width_bounds['min'],
                      self.width_bounds['max'], self.width_bounds['min'], 'black')
        self.add_line(self.height_bounds['min'], self.height_bounds['min'],
                      self.height_bounds['min'], self.height_bounds['max'], 'black')

        for i in range(11):
            y = self.height_bounds['min'] + (self.height_bounds['len'] / 10) * i
            self.add_line(self.width_bounds['min'], y, self.width_bounds['min'] - 20, y, 'black')
            self.add_text(5, y + 5, 0, '{0:.2f}'.format(y_axis[i]))

        for i in range(11):
            x = self.width_bounds['min'] + (self.width_bounds['len'] / 10) * i
            self.add_line(x, self.height_bounds['min'], x, self.height_bounds['min'] - 20, 'black')
            self.add_text(x - self.width_bounds['len'] / 10, 30, 45, '{0:.2f}'.format(x_axis[i]))

    def add_text(self, x, y, angle, text, size=25):
        self.texts.append("<text x='{0}' y='{1}' font-size='{2}' transform='rotate({3}, {0}, {1})'>{4}</text>" \
                          .format(x, y, size, angle, text))

    def add_line(self, x1, y1, x2, y2, color, width=5):
        self.lines.append("<line x1='{0}' y1='{1}' x2='{2}' y2='{3}' style='stroke:{5};stroke-width:{4}'/>" \
                          .format(x1, y1, x2, y2, width, color))

    def add_rectangle(self, x, y, w, h, color):
        self.regions.append("<rect x='{0}' y='{1}' width='{2}' height='{3}' fill='{4}' />" \
                            .format(x, y, w, h, color))

    def add_point(self, x, y, color):
        self.points.append("<circle cx='{0}' cy='{1}' r='{2}' stroke='{4}' stroke-width='{3}' fill='{4}' />" \
                           .format(x, y, 3, 3, color))

    def add_legend_points(self, min_v, max_v):
        x = self.width_bounds['min'] + 100
        y = self.height_bounds['max'] + 100
        self.add_rectangle(x, self.height_bounds['max'] + 30, 250, 25, 'url(%23gradient)')
        self.add_line(x, self.height_bounds['max'] + 55, x + 250, self.height_bounds['max'] + 55, 'black', 3)

        values = [min_v, (min_v + max_v) / 2, max_v]

        for i in range(len(values)):
            self.add_line(x + i * 125, self.height_bounds['max'] + 55, x + i * 125, self.height_bounds['max'] + 65,
                          'black', 3)
            self.add_text(x - 30 + i * 125, y - 10, 0, '%.2f' % values[i])


    def load_points(self, points, x, y, min_val, max_val, normalisation=True):
        self.add_legend_points(min_val, max_val)
        for point in points:
            p = point.value
            x_cor = fit_to_picture(normalise(point.projection(x), self.bounds['x_max'], self.bounds['x_min']),
                                   self.width_bounds['len'], self.width_bounds['min'])
            y_cor = fit_to_picture(normalise(point.projection(y), self.bounds['y_max'], self.bounds['y_min']),
                                   self.height_bounds['len'], self.height_bounds['min'])
            if normalisation:
                p = normalise(p, min_val, max_val)
            self.add_point(x_cor, y_cor, colorify(p))


def normalise(value, min_value, max_value):
    return (max_value - value) / (max_value - min_value)


def fit_to_picture(value, multi, add):
    return value * multi + add


def colorify(value):
    if value < 0.5:
        return 'rgb(255,{0},0)'.format(int(255 * (1 - normalise(value, 0, 0.5))))
    return 'rgb({0},{1},0)'.format(int(255 * (normalise(value, 0.5, 1))), 128 + int(128 * (normalise(value, 0.5, 1))))
