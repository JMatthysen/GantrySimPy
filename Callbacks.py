from main import *


def render_callback(sender, data):
    for i in range(3):
        vector = [0, 0, 0]

        slider_name = f"slider_{i}"
        if is_item_active(slider_name):
            val             = get_value(slider_name)
            vector[i]  = val

            event_bus.post_event("translation_event", vector)
        else:
            set_value(slider_name, 0)


def full_screen():
    set_main_window_pos(0, 0)
    set_main_window_size(1920, 1080)


set_render_callback(render_callback)
full_screen()
start_dearpygui(primary_window=gui_window.name)