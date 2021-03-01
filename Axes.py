from EventFramework import EventHandler
from AxisShapes import *


class Axis(EventHandler):
    def __init__(self, name, origin, shape_type, axis_influence_level, event_bus):
        self.name           = name
        self.origin         = origin
        self.shape_type     = shape_type
        self.coordinates    = list()
        self._axis_level    = axis_influence_level  # this determines wether or not the axis will be effected
                                          # by a mvmt from another axis. Higher numbers are effected by lower numbers
        self.event_bus      = event_bus

        self._initialize_subscriptions()

    def _initialize_subscriptions(self):
        self.subscribe(self.event_bus, "translation_event")

    def subscribe(self, event_bus, event_name):
        event_bus.subscribe(self, event_name)


"""

ex:
name        = "y_axis"      string
origin      = [0, 1, 0]     list(float) 
dimensions  = [1, 1, 1]     list(depth(x), width(y), height(z))
shape_type  = "rectangle"   string

axis_influence_levels:
                        x_axis = 0
                        y_axis = 1
                        z_axis = 2
                        r_axis = 3
"""


class LinearAxis(Axis):
    def __init__(self, name, origin, dimensions, axis_influence_level, event_bus, shape_type="rectangle"):
        Axis.__init__(self, name, origin, shape_type, axis_influence_level, event_bus)
        self.shape = Rectangle(dimensions[0], dimensions[1], dimensions[2])
        self.initialize_shape()

    def on_event(self, event_name, data):
        if event_name == "translation_event":
            self._translation_event(data)

    def _translation_event(self, data):
        #  data must be passed in a list (x, y, z)

        for i, axis_change in enumerate(data):
            if self._axis_level > i and axis_change != 0:
                self.update_coordinates(data)

            else:
                pass

    def update_coordinates(self, xyz):
        for i, point in enumerate(self.coordinates):
            self.coordinates[i][0] += xyz[0]
            self.coordinates[i][1] += xyz[1]
            self.coordinates[i][2] += xyz[2]

        self.event_bus.post_event("position_change_event", self.name)

    def initialize_shape(self):
        x       = self.origin[0]
        y       = self.origin[1]
        z       = self.origin[2]
        depth   = self.shape.depth
        width   = self.shape.width
        height  = self.shape.height

        self.coordinates.append(self.origin)
        self.coordinates.append([x, y, z + height])
        #  point 1 = originx, originy z+height
        self.coordinates.append([x, y + width, z + height])
        #  point 2 = originx, y + width, z+height
        self.coordinates.append([x, y + width, z])
        #  point 3 = originx, y + width, originz
        self.coordinates.append([x + depth, y, z])
        #  point 4 = x + depth, originy, originz
        self.coordinates.append([x + depth, y, z + height])
        #  point 5 = x + depth, originy, z + height
        self.coordinates.append([x + depth, y + width, z + height])
        #  point 6 = x + depth, y + width, z + height
        self.coordinates.append([x + depth, y + width, z])
        #  point 7 = x + depth, y + width, originz
