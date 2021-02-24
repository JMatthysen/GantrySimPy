from EventFramework import EventHandler


class Axis(EventHandler):
    def __init__(self):
        self.name           = ""
        self.shape_type     = ""
        self.shape          = None
        self.coordinates    = list(list())


