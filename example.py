from grbltouchscreencontroller import grblcontroller

controller = grblcontroller.Controller(port="/dev/cu.usbmodemFA131")
controller.demo_move()
controller.demo_tab()

