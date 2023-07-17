import serial
import time
import constants

class Controller:

    def __init__(self,port) -> None:
        self.arduino = serial.Serial(port=port,baudrate=constants.DEFAULT_BAUD)
        self._initialize()
        self._home()
    
    def read(self,lines):
        output_lines = []
        while (True):
            if self.arduino.in_waiting > 0:
                output_lines.append(self.arduino.read(self.arduino.in_waiting).decode(constants.DEFAULT_ENCODING))
                time.sleep(0.01)
            else:
                break
        return output_lines
    
    def send(self,command):
        self._write(command)
    
    def _initialize(self):
        self._write(constants.NEW_LINE_CHARACTER)

    def _write(self,input):
        self.arduino.write(bytes(str(input) + constants.NEW_LINE_CHARACTER,constants.DEFAULT_ENCODING))
        time.sleep(constants.DEFAULT_SLEEP)
        self.arduino.flushInput()

    def _home(self):
        self._write(constants.GRBL_HOME_COMMAND)
