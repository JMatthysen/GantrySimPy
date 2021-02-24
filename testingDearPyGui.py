from dearpygui.core import *
from dearpygui.simple import *


DRAWING = "TestingDrawing"

NEGLIMIT = 0
POSLIMIT = 1000

class Rectangle:
    def __init__(self, width, height, origin):
        self.width  = width
        self.height = height
        self.origin = origin

        self.p_min  = origin
        self.p_max  = [origin[0] + width, origin[1] + height]

    def update_rectangle(self, x_shift):
        self.limit_check(x_shift)

        draw_rectangle(DRAWING, pmin=self.p_min, pmax=self.p_max, color=[233, 100, 40, 230], fill=[233, 100, 40, 255])

    def limit_check(self, x_shift):
        if self.p_min[0] + x_shift <= NEGLIMIT or self.p_max[0] + x_shift >= POSLIMIT:
            self.p_min[0] = NEGLIMIT
            self.p_max[0] = POSLIMIT
        else:
            self.p_min[0] += x_shift
            self.p_max[0] += x_shift

add_data("PMIN", [10, 10])
add_data("PMAX", [50, 100])


def update_rectangle_callback(sender, data):
    val = get_value(sender)
    update_canvas(val)



def update_canvas(val):
    clear_drawing(DRAWING)
    rectangle = data
    rectangle.update_rectangle(val)


with window(name="TestingWindow", autosize=True):
    add_drawing(drawing_name, width=1000, height=200)
    update_rectangle(0)

    add_slider_float("x_axis_control", min_value=-10, max_value=10, callback=update_rectangle_callback)


def render_callback(sender, data):
    slider_name = "x_axis_control"
    if is_item_active(slider_name):
        val = get_value(slider_name)
        update_rectangle(val)

    else:
        set_value(slider_name, 0)


set_render_callback(render_callback)
start_dearpygui()
