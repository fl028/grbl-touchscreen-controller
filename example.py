from grbltouchscreencontroller import grblcontroller

controller = grblcontroller.Controller()

#controller.refresh_settings() # use this to initaly set settings
controller.home()
controller.demo_tab()

for i in range(3):
    controller.demo_move_topright()
    controller.demo_move_topleft()
    controller.demo_move_middle()
    controller.demo_tab()
    controller.demo_move_bottomleft()
    controller.demo_move_bottomright()

