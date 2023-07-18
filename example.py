from grbltouchscreencontroller import grblcontroller

controller = grblcontroller.Controller()

for i in range(10):
    controller.demo_move()
    controller.demo_tab()

