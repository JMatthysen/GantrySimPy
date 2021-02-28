from dearpygui.core import *
from dearpygui.simple import *


DRAWING = "TestingDrawing"

NEGLIMIT = 0
POSLIMIT = 1000


class Rectangle:
    def __init__(self, width, height, origin, color):
        self.width  = width
        self.height = height
        self.origin = origin
        self.color  = color
        self.p_min  = origin
        self.p_max  = [origin[0] + width, origin[1] + height]

    def update_rectangle(self, x_shift):
        if self.neg_limit_check(x_shift):
            self.p_min[0] = NEGLIMIT
            self.p_max[0] = NEGLIMIT + self.width

        elif self.pos_limit_check(x_shift):
            self.p_min[0] = POSLIMIT - self.width
            self.p_max[0] = POSLIMIT

        else:
            self.p_min[0] += x_shift
            self.p_max[0] += x_shift

    def add_rectangle(self):
        draw_rectangle(DRAWING, pmin=self.p_min, pmax=self.p_max, color=self.color, fill=self.color)

    def neg_limit_check(self, x_shift):
        if self.p_min[0] + x_shift <= NEGLIMIT:
            return True
        else:
            return False

    def pos_limit_check(self, x_shift):
        if self.p_max[0] + x_shift >= POSLIMIT:
            return True
        else:
            return False


rect_a = Rectangle(50, 100, [10, 10], [50, 168, 94, 255])
rect_b = Rectangle(100, 50, [300, 60], [104, 12, 107, 255])
rect_c = Rectangle(40, 40, [400, 70], [245, 250, 1, 150])
rect_d = Rectangle(20, 20, [100, 90], [30, 30, 30, 255])
rect_e = Rectangle(500, 20, [200, 90], [80, 85, 90, 100])


RECTANGLES = [rect_a, rect_b, rect_c, rect_d, rect_e]


def update_rectangle_callback(sender, data):
    val = get_value(sender)
    rectangle = data
    rectangle.update_rectangle(val)
    update_canvas()


def update_canvas():
    clear_drawing(DRAWING)
    for rect in RECTANGLES:
        rect.add_rectangle()


with window(name="TestingWindow", autosize=True):
    add_drawing(DRAWING, width=1000, height=200)
    update_canvas()
    for i in range(len(RECTANGLES)):
        add_slider_float(f"rect_{i}_control", min_value=-10, max_value=10, callback=update_rectangle_callback)


def render_callback(sender, data):
    for i, rect in enumerate(RECTANGLES):
        slider_name = f"rect_{i}_control"
        if is_item_active(slider_name):
            val = get_value(slider_name)
            RECTANGLES[i].update_rectangle(val)
        else:
            set_value(slider_name, 0)
    update_canvas()


set_render_callback(render_callback)

start_dearpygui()
