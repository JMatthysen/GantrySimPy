"""

simple shapes used to represent a gantry axis

"""


class Rectangle:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

class Circle:
    def __init__(self, radius):
        self.radius = radius