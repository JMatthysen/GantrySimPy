from dearpygui.core import *
from dearpygui.simple import *
from EventFramework import EventHandler


class Entity:
    def __init__(self, name, shape, points, color):
        self.name   = name
        self.shape  = shape
        self.points = points
        self.color  = color


class CanvasView(EventHandler):
    def __init__(self, name, width, height):
        self.name       = name
        self.width      = width
        self.height     = height
        self.entities   = list()

    def on_event(self, event):
        pass

    def initialize_canvas(self):
        add_drawing(self.name, width=self.width, height=self.height)

    def refresh_canvas(self):
        clear_drawing(self.name)

        for entity in self.entities:
            self.draw_entity(entity)

    def add_entity(self, name, shape, points, color):
        self.entities.append(Entity(name, shape, points, color))

    def draw_entity(self, entity):
        if entity.shape == "rectangle":
            draw_rectangle(self.name, entity.points[0], entity.points[1],
                           entity.color, fill=entity.color)
        else:
            print(f"Entity's ({entity.name}) shape not supported {entity.shape}")



