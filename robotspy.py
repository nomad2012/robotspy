#!/usr/bin/env python
"""robotspy.py - control my robot spy hexapod
"""

import serial
from . import maestro as m
    
def main():
    argv = sys.argv
    if len(argv) > 1:
        port = argv[1]
    else:
        port = 'usb-Pololu_Corporation_Pololu_Mini_Maestro_24-Channel_USB_Servo_Controller_00149355-if00'

    maestro = serial.Serial(port=port, baudrate=57600, timeout=1)

if __name__ == '__main__':
    main()
