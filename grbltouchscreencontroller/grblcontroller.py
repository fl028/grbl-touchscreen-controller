import os
import serial
import time
import grbltouchscreencontroller.constants as const

class Controller:

    def __init__(self) -> None:
        self._initialize()
        

    def __del__(self):
        try:
            self.arduino.close()
        except:
            pass
        print("Connection closed")

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
        
    def refresh_settings(self):
        for key, value in const.GRBL_CONFIG.items():
            print(f"Setting: {key}")
            self._send_and_receive(value + const.NEW_LINE_CHARACTER)

    def home(self):
        print("Home")
        self._send_and_receive(const.GRBL_HOME_COMMAND + const.NEW_LINE_CHARACTER)
        self._send_and_receive(const.GRBL_ZERO_COMMAND + const.NEW_LINE_CHARACTER)

    def demo_move_topright(self):
        print("Move topright")
        self._send_and_receive(const.GRBL_MOVE_COMMAND_1 + const.NEW_LINE_CHARACTER)

    def demo_move_topleft(self):
        print("Move topleft")
        self._send_and_receive(const.GRBL_MOVE_COMMAND_2 + const.NEW_LINE_CHARACTER)

    def demo_move_bottomleft(self):
        print("Move bottomleft")
        self._send_and_receive(const.GRBL_MOVE_COMMAND_3 + const.NEW_LINE_CHARACTER)

    def demo_move_bottomright(self):
        print("Move bottomright")
        self._send_and_receive(const.GRBL_MOVE_COMMAND_4 + const.NEW_LINE_CHARACTER)

    def demo_move_middle(self):
        print("Move middle")
        self._send_and_receive(const.GRBL_MOVE_COMMAND_5 + const.NEW_LINE_CHARACTER)


    def demo_tab(self):
        print("Tab")
        self._send_and_receive(command = const.GRBL_TAB_COMMAND_DOWN + const.NEW_LINE_CHARACTER, sleep=const.SLEEP_MINI)
        self._send_and_receive(command = const.GRBL_TAB_COMMAND_UP + const.NEW_LINE_CHARACTER)
        
