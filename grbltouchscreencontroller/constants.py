DEVICE_DEV_PATH = "/dev/"
DEVICE_CALLINGUNIT_NAME = "cu.usbmodem"

SLEEP_MINI = 0.09
SLEEP_DEFAULT = 0.5
SLEEP_LONG = 2

NEW_LINE_CHARACTER = "\n"
DEFAULT_BAUD = 115200
DEFAULT_ENCODING = "utf-8"
GRBL_WAKEUP_COMMAND = "\r\n\r\n"
GRBL_HOME_COMMAND = "$H"
GRBL_ZERO_COMMAND = "G92 X0 Y0"


GRBL_TAB_COMMAND_UP = "m3 s90"
GRBL_TAB_COMMAND_DOWN = "m5"

GRBL_MOVE_COMMAND_1 = "G1 X198 Y0 F12000"
GRBL_MOVE_COMMAND_2 = "G1 X198 Y263 F12000"
GRBL_MOVE_COMMAND_3 = "G1 X0 Y263 F12000"
GRBL_MOVE_COMMAND_4 = "G1 X0 Y0 F12000"
GRBL_MOVE_COMMAND_5 = "G1 X99 Y131.5 F12000" # middle

GRBL_CONFIG = {
    "Step Pulse": "$0=10",
    "Step Idle Delay": "$1=25",
    "Step Port Invert Mask": "$2=0",
    "Dir Port Invert Mask": "$3=0",
    "Step Enable Invert": "$4=0",
    "Limit Pins Invert": "$5=0",
    "Probe Pin Invert": "$6=0",
    "Status Report Mask": "$10=3",
    "Junction Deviation": "$11=0.010",
    "Arc Tolerance": "$12=0.002",
    "Report Inches": "$13=0",
    "Soft Limits": "$20=1",
    "Hard Limits": "$21=0",
    "Homing Cycle": "$22=1",
    "Homing Dir Invert Mask": "$23=3",
    "Homing Feed": "$24=6000.000",
    "Homing Seek": "$25=9000.000",
    "Homing Debounce": "$26=4",
    "Homing Pull-off": "$27=3.000",
    "X Step/mm": "$100=20",
    "Y Step/mm": "$101=20",
    "Z Step/mm": "$102=250.000",
    "X Max Rate": "$110=12000.000",
    "Y Max Rate": "$111=12000.000",
    "Z Max Rate": "$112=500.000",
    "X Acceleration": "$120=500.000",
    "Y Acceleration": "$121=500.000",
    "Z Acceleration": "$122=10.000",
    "X Max Travel": "$130=215.000",
    "Y Max Travel": "$131=300.000",
    "Z Max Travel": "$132=200.000",
}

