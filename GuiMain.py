from dearpygui.core import *
from dearpygui.simple import *
from EventFramework import EventHandler


class Entity:
    def __init__(self, axis, color):
        self.axis   = axis
        self.name   = self.axis.name
        self.shape  = self.axis.shape_type
        self.color  = color


class Entity3D(Entity):
    def __init__(self, axis, color):
        Entity.__init__(self, axis, color)

        self.sides = list(list())
        self.color_border = [255, 255, 255, 255]

        self._initialize_sides()

    def _initialize_sides(self):
        self.sides.append([0, 1, 2, 3, 0])
        self.sides.append([0, 1, 5, 4, 0])
        self.sides.append([0, 3, 7, 4, 0])

        self.sides.append([6, 7, 4, 5, 6])
        self.sides.append([6, 7, 3, 2, 6])
        self.sides.append([6, 5, 1, 2, 6])


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

        elif event_name == "view_screen_translation_event":
            self._translate_view_screen(data)

        elif event_name == "view_screen_rotation_event":
            self._rotate_view_screen()

    def _initialize_subscriptions(self):
        self.subscribe(self.event_bus, "position_change_event")
        self.subscribe(self.event_bus, "view_screen_translation_event")
        self.subscribe(self.event_bus, "view_screen_rotation_event")

    def subscribe(self, event_bus, event_name):
        event_bus.subscribe(self, event_name)

    def _update_drawing_event(self):
        self._refresh_canvas()

    def _translate_view_screen(self, data):
        pass

    def _rotate_view_screen(self, data):
        pass

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

            with group("controls_row", width=800, horizontal=True):
                pass
            self._add_sliders()
            self._add_view_screen_controls()
            with group("canvas_row", horizontal=True):
                pass

    def _add_sliders(self):
        with group("slider_group", parent="controls_row", width=100):
            for i in range(3):
                add_slider_float(f"slider_{i}", min_value=-10, max_value=10, width=50)

    def _add_view_screen_controls(self):
        with group("view_port_controls", parent="controls_row", width=100):
            for i in range(3):
                add_slider_float(f"view_screen_control_{i}", min_value=-10, max_value=10, width=50 )