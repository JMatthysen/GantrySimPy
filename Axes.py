from EventFramework import EventHandler
from AxisShapes import *


class Axis(EventHandler):
    def __init__(self, name, origin, shape_type):
        self.name           = name
        self.origin         = origin
        self.shape_type     = shape_type
        self.coordinates    = list()


"""

ex:
name        = "y_axis"      string
origin      = [0, 1, 0]     list(float) 
dimensions  = [1, 1, 1]     list(depth(x), width(y), height(z))
shape_type  = "rectangle"   string
"""


class LinearAxis(Axis):
    def __init__(self, name, origin, dimensions, shape_type = "rectangle"):
        Axis.__init__(self, name, origin, shape_type)
        self.shape = Rectangle(dimensions[0], dimensions[1], dimensions[2])

        self.update_coordinates(dimensions)

    def on_event(self, event_type, event_name, data):
        if event_type == "translate_event":
            self.update_origin(data)

    def update_origin(self, xyz):
        for i, dimension in enumerate(self.origin):
            dimension += xyz[i]

    def update_coordinates(self, xyz):

        for i, point in enumerate(self.coordinates):
            self.coordinates[i][0] += xyz[0]
            self.coordinates[i][1] += xyz[1]
            self.coordinates[i][2] += xyz[2]

