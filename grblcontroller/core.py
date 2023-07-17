import serial
import time
import grblcontroller.constants as const

class Controller:

    def __init__(self, port) -> None:
        self.arduino = serial.Serial(port=port, baudrate=const.DEFAULT_BAUD)
        self._initialize()
        self._home()

    def __del__(self):
        self.arduino.close()
        print("Connection closed")

    def read(self):
        output_lines = []
        while True:
            if self.arduino.in_waiting > 0:
                output_lines.append(self.arduino.read(self.arduino.in_waiting).decode(const.DEFAULT_ENCODING))
                time.sleep(const.DEFAULT_SLEEP)
            else:
                break
        print("Read: " + str(output_lines))
        return output_lines

    def send(self, command):
        self._write(command)
        return self.read()  # Wait for read output after sending the command

    def _initialize(self):
        print("Init")
        self.arduino.close()
        self.arduino.open()
        self._get_port_state()
        self._write(const.NEW_LINE_CHARACTER)
        self.read()

    def _get_port_state(self):
        self.state = self.arduino.is_open
        if not self.state:
            raise Exception("Port closed")
        print("Port state: " + str(self.state))

    def _write(self, input):
        self.arduino.write(bytes(input + const.NEW_LINE_CHARACTER, const.DEFAULT_ENCODING))
        time.sleep(const.DEFAULT_SLEEP)
        self.arduino.flushInput()
        time.sleep(const.DEFAULT_SLEEP)

    def _home(self):
        print("Home")
        self.send(const.GRBL_HOME_COMMAND)
        self.send(const.GRBL_ZERO_COMMAND)
