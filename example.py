from grbltouchscreencontroller import grblcontroller

controller = grblcontroller.Controller()

controller.refresh_settings() # use this to initially set settings
controller.home()
controller._tab() # initially lift pen

for i in range(2):
    controller.demo()

controller.sleep_position()