import serial
import time
import grbltouchscreencontroller.constants as const

class Controller:

    def __init__(self, port) -> None:
        self.arduino = serial.Serial(port=port, baudrate=const.DEFAULT_BAUD)
        self._initialize()
        self._home()

    def __del__(self):
        try:
            self.arduino.close()
        except:
            pass
        print("Connection closed")

    def read(self):
        output_lines = []
        while True:
            while self.arduino.in_waiting == 0:
                time.sleep(0.02)
            output_lines.append(self.arduino.read(self.arduino.in_waiting).decode(const.DEFAULT_ENCODING))
            if self.arduino.in_waiting == 0:
                break
        time.sleep(const.DEFAULT_SLEEP)
        print("Read: " + str(output_lines))
        return output_lines

    def send_and_receive(self, command, check=True):
        self._write(command)
        output = self.read()

        if check:
            if "ok" not in output[0]:
                raise serial.SerialException("Not ok")

    def _initialize(self):
        print("Init")
        self.arduino.close()
        self.arduino.open()
        self._get_port_state()
        self.send_and_receive(const.GRBL_WAKEUP_COMMAND,False)

    def _get_port_state(self):
        self.state = self.arduino.is_open
        if not self.state:
            raise serial.SerialException("Port closed")
        print("Port state: " + str(self.state))

    def _write(self, input):
        print("Write: " + str(input).strip())
        self.arduino.write(bytes(input, const.DEFAULT_ENCODING))
        self.arduino.flushInput()
        time.sleep(const.DEFAULT_SLEEP)
        

    def _home(self):
        print("Home")
        self.send_and_receive(const.GRBL_HOME_COMMAND + const.NEW_LINE_CHARACTER)
        self.send_and_receive(const.GRBL_ZERO_COMMAND + const.NEW_LINE_CHARACTER)

    def demo_move(self):
        print("Move")
        self.send_and_receive(const.GRBL_MOVE_COMMAND_2 + const.NEW_LINE_CHARACTER)
        self.send_and_receive(const.GRBL_MOVE_COMMAND_1 + const.NEW_LINE_CHARACTER)

    def demo_tab(self):
        print("Tab")
        self.send_and_receive(const.GRBL_TAB_COMMAND_1 + const.NEW_LINE_CHARACTER)
        self.send_and_receive(const.GRBL_TAB_COMMAND_2 + const.NEW_LINE_CHARACTER)
        
        
