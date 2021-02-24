"""

simple shapes used to represent a gantry axis

"""


class Rectangle:
    def __init__(self, depth, width, height):
        self.depth  = depth     # x axis
        self.width  = width     # y axis
        self.height = height    # z axis


class Circle:
    def __init__(self, radius):
        self.radius = radius
