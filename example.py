from grbltouchscreencontroller import grblcontroller

demo_tab_screen_locations = {
    "top_right_1": (838, 31),
    "top_right_2": (839, 84),
    "top_right_3": (839, 134),
    "bottom_left_1": (63, 598),
    "bottom_left_2": (39, 505)
}

controller = grblcontroller.Controller(screensize_px=(874,656),refresh_settings=False)
controller.home()

for desc,loc in demo_tab_screen_locations.items():
    print(desc)
    controller.touch_display(loc)
