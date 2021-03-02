from Axes import *
from EventFramework import *
from GuiMain import *
from Callbacks import *
from ViewScreen import *


event_bus = EventBus()

x_axis      = LinearAxis("x_axis", [100, 310, 400], [300, 30, 30], 0, event_bus)
x2_axis     = LinearAxis("x2_axis", [100, 580, 400], [300, 30, 30], 0, event_bus)

y_axis      = LinearAxis("y_axis", [100, 310, 370], [30, 300, 30], 1, event_bus)

z_axis      = LinearAxis("z_axis", [130, 310, 200], [30, 30, 200], 2, event_bus)

r_axis      = LinearAxis("r_axis", [110, 300, 220], [20, 50, 50], 3, event_bus)

gui_window  = GUIWindow("gui_window", 1100, 750)

"""front_view  = FrontView("front_view", (0, 1, 1), 750, 500, "canvas_row", event_bus)
front_view.add_entity(x_axis, (255, 200, 30, 255))
front_view.add_entity(x2_axis, (255, 200, 30, 255))
front_view.add_entity(z_axis, (97, 235, 52, 255))
front_view.add_entity(y_axis, (235, 222, 52, 255))
front_view.add_entity(r_axis, (30, 200, 100, 255))

side_view = SideView("side_view", (1, 0, 1), 750, 500, "canvas_row", event_bus)
side_view.add_entity(x_axis, (255, 200, 30, 255))
side_view.add_entity(x2_axis, (255, 200, 30, 255))
side_view.add_entity(y_axis, (235, 222, 52, 255))
side_view.add_entity(z_axis, (97, 235, 52, 255))
side_view.add_entity(r_axis, (30, 200, 100, 255))"""

view_screen = ViewScreen("view_screen", (0, 0, 0), 800, 600, gui_window.name, event_bus,
                         100, [400, 400, 400], [880, 1040, 400], [400, 400, -200])
view_screen.add_entity(x_axis, (255, 200, 30, 255))
view_screen.add_entity(x2_axis, (255, 200, 30, 255))
view_screen.add_entity(y_axis, (235, 222, 52, 255))
view_screen.add_entity(r_axis, (30, 200, 100, 255))
view_screen.add_entity(z_axis, (97, 235, 52, 255))
