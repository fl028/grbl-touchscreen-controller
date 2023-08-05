import os
import serial
import time
import grbltouchscreencontroller.constants as const

class Controller:

    def __init__(self,screensize_px,refresh_settings=False) -> None:
        """
        screensize_px = current (width,height) in px of tablet screen
        """
        if refresh_settings:
            self._refresh_settings() # use this to initially update settings

        self.screensize_px = screensize_px
        self._initialize()
        self._calculate_screen_scale()

    def __del__(self):
        self.sleep_position()
        try:
            self.arduino.close()
        except:
            pass
        print("Connection closed")

    def _calculate_screen_scale(self):
        print("Calculate screen scale")
        self.scale_x = round(const.GRBL_COORDINATE_MAX_Y / self.screensize_px[0],3)  
        self.scale_y = round(const.GRBL_COORDINATE_MAX_X / self.screensize_px[1],3)
        print(f"Calculated scaling: scale_x: {self.scale_x} scale_y: {self.scale_y}")

    def _search_arduino_port(self):
        for f in os.listdir(const.DEVICE_DEV_PATH):
            if const.DEVICE_CALLINGUNIT_NAME in f:
                arduino_port = str(const.DEVICE_DEV_PATH + f)
                print("Arduino port: " + arduino_port)
                return arduino_port
        raise serial.SerialException("Arduino not found")
            
    def _read(self,check,sleep):
        print("Read (Checkmode: " + str(check) + ")")
        output_lines = []
        while True:
            while self.arduino.in_waiting == 0:
                time.sleep(const.SLEEP_MINI)
            output_lines.append(self.arduino.read(self.arduino.in_waiting).decode(const.DEFAULT_ENCODING))
            if self.arduino.in_waiting == 0:
                break
        time.sleep(sleep)

        if check:
            print("Check: " + str(output_lines[0]).strip())
            if "ok" not in output_lines[0]:
                raise serial.SerialException("Not ok")
        else:
            print("Read: " + str(output_lines))

    def _send_and_receive(self, command, check=True, sleep= const.SLEEP_DEFAULT):
        self._write(command, sleep)
        self._read(check, sleep)

    def _initialize(self):
        print("Init")
        self.arduino = serial.Serial(port=self._search_arduino_port(), baudrate=const.DEFAULT_BAUD)
        self.arduino.close()
        self.arduino.open()
        self._check_port_state()
        self._send_and_receive(const.GRBL_WAKEUP_COMMAND,False)
        time.sleep(const.SLEEP_LONG)

    def _check_port_state(self):
        self.state = self.arduino.is_open
        if not self.state:
            raise serial.SerialException("Port closed")
        print("Port state: " + str(self.state))

    def _write(self, input, sleep):
        print("Write: " + str(input).strip())
        self.arduino.write(bytes(input, const.DEFAULT_ENCODING))
        self.arduino.flushInput()
        time.sleep(sleep)
        
    def _refresh_settings(self):
        print("Refresh grbl settings")
        for key, value in const.GRBL_CONFIG.items():
            print(f"Setting: {key}")
            self._send_and_receive(value + const.NEW_LINE_CHARACTER)

    def home(self):
        print("Home")
        self._send_and_receive(const.GRBL_HOME_COMMAND + const.NEW_LINE_CHARACTER)
        self._send_and_receive(const.GRBL_ZERO_COMMAND + const.NEW_LINE_CHARACTER)
        self._tab() # initially lift pen

    def sleep_position(self):
        print("Sleep Position")
        self._move(const.GRBL_CORDS_SLEEP_POSITION)
        
    def _tab(self):
        print("Tab")
        self._send_and_receive(command = const.GRBL_TAB_COMMAND_DOWN + const.NEW_LINE_CHARACTER, sleep=const.SLEEP_MINI)
        self._send_and_receive(command = const.GRBL_TAB_COMMAND_UP + const.NEW_LINE_CHARACTER)

    def _move(self,grbl_cords):
        print("Move")
        grbl_cmd = self._build_grbl_move_command(grbl_cords)
        self._send_and_receive(grbl_cmd + const.NEW_LINE_CHARACTER)

    def _build_grbl_move_command(self,grbl_cords):
        print("Build grbl command")
        grbl_command = "G1 X"+str(grbl_cords[0])+" Y"+str(grbl_cords[1])+" F" + str(const.GRBL_DEFAULT_MOVEMENT_SPEED)
        return grbl_command

    def touch_display(self,screen_coordinate_px):
        grbl_cords = self._convert_screen_location_to_grbl_location(screen_coordinate_px)
        self._move(grbl_cords)
        self._tab()

    def _convert_screen_location_to_grbl_location(self, image_point):
        image_x, image_y = image_point
        
        # Invert the y-coordinate
        Y_inverted = self.screensize_px[1] - image_y
        
        # Map the image point to cartesian coordinates
        grbl_x = Y_inverted * self.scale_x  # Swap X and Y
        grbl_y = image_x * self.scale_y  # Swap X and Y
        
        # Mirror the cartesian coordinates along the X-axis
        grbl_y = const.GRBL_COORDINATE_MAX_Y - grbl_y
        
        return round(grbl_x,2), round(grbl_y,2)

    
