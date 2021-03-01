from dearpygui.core import *
from dearpygui.simple import *
from EventFramework import EventHandler


class Entity:
    def __init__(self, axis, color):
        self.axis   = axis
        self.name   = self.axis.name
        self.shape  = self.axis.shape_type
        self.color  = color


class CanvasView(EventHandler):
    def __init__(self, name, axes, width, height, parent, event_bus):
        self.name       = name
        self.axes       = axes
        self.width      = width
        self.height     = height
        self.parent     = parent
        self.event_bus  = event_bus
        self.entities   = list()

        self._initialize_canvas()
        self._initialize_subscriptions()
        self._add_labels()

    def on_event(self, event_name, data):
        if event_name == "position_change_event":
            self._update_drawing_event()

    def _initialize_subscriptions(self):
        self.subscribe(self.event_bus, "position_change_event")

    def subscribe(self, event_bus, event_name):
        event_bus.subscribe(self, event_name)

    def _update_drawing_event(self):
        self._refresh_canvas()

    def _initialize_canvas(self):
        add_drawing(self.name, parent=self.parent, width=self.width, height=self.height)

    def _refresh_canvas(self):
        clear_drawing(self.name)

        self._refresh_entities()

        self._add_labels()

    def add_entity(self, axis, color):
        self.entities.append(Entity(axis, color))
        self._draw_entity(self.entities[-1])

    def _refresh_entities(self):
        for entity in self.entities:
            self._draw_entity(entity)

    def _draw_entity(self, entity):
        pass

    def _add_labels(self):
        pass

    @staticmethod
    def _get_usable_points(xyz, axes):
        result = list()
        for i, point in enumerate(axes):
            if point:
                result.append(xyz[i])
        return result


class FrontView(CanvasView):
    def __init__(self, name, axes, width, height, parent, event_bus):
        CanvasView.__init__(self, name, axes, width, height, parent, event_bus)

    def _draw_entity(self, entity):
        if entity.shape == "rectangle":
            rect_min = self._get_usable_points(entity.axis.coordinates[1], self.axes)

            rect_max = self._get_usable_points(entity.axis.coordinates[3], self.axes)

            draw_rectangle(self.name, pmin=rect_min, pmax=rect_max,
                           color=entity.color, fill=entity.color)
        else:
            print(f"Entity's ({entity.name}) shape not supported {entity.shape}")

    def _add_labels(self):
        # Title
        draw_text(self.name, [10, 10], self.name, size=20)

        # vertical_axis
        draw_text(self.name, [0, self.height/2], "Z-AXIS", size=20)

        # horizontal_axis
        draw_text(self.name, [self.width/2, self.height - 20], "Y-AXIS", size=20)


class SideView(CanvasView):
    def __init__(self, name, axes, width, height, parent, event_bus):
        CanvasView.__init__(self, name, axes, width, height, parent, event_bus)

    def _draw_entity(self, entity):
        if entity.shape == "rectangle":
            rect_min = self._get_usable_points(entity.axis.coordinates[2], self.axes)

            rect_max = self._get_usable_points(entity.axis.coordinates[7], self.axes)

            draw_rectangle(self.name, pmin=rect_min, pmax=rect_max,
                           color=entity.color, fill=entity.color)
        else:
            print(f"Entity's ({entity.name}) shape not supported {entity.shape}")

    def _add_labels(self):
        # Title
        draw_text(self.name, [10, 10], self.name, size=20)

        # vertical_axis
        draw_text(self.name, [0, self.height / 2], "Z-AXIS", size=20)

        # horizontal_axis
        draw_text(self.name, [self.width / 4, self.height - 20], "X-AXIS", size=20)


class GUIWindow:
    def __init__(self, name, width, height):
        self.name   = name
        self.width  = width
        self.height = height

        self._initialize_gui()

    def _initialize_gui(self):
        with window(self.name, width=self.width, height=self.height):
            self._add_sliders()
            with group("canvas_row", horizontal=True):
                pass

    def _add_sliders(self):
        with group("slider_group", parent=self.name):
            for i in range(3):
                add_slider_float(f"slider_{i}", min_value=-10, max_value=10)