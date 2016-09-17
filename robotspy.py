#!/usr/bin/env python
"""robotspy.py - control my robot spy hexapod
"""

import serial
import sys
import time
import maestro as m


legs = [[0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [9, 10, 11],
        [12, 13, 14],
        [15, 16, 17]]

leg_angles = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0],
              [0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

leg_zero_positions = [[6000, 1459 * 4, 6000],
                      [6000, 1516 * 4, 6000],
                      [6000, 1384 * 4, 6000],
                      [6000, 1397 * 4, 6000],
                      [6000, 1467 * 4, 6000],
                      [6000, 1450 * 4, 6000]]


def degrees_to_target(angle):
    """convert angle in degrees to servo target in units of 0.25us
    0 degrees = 6000
    -60 degrees = 4000
    60 degrees = 8000"""
    return int(round(angle * 2000.0 / 60.0)) + 6000


def init_legs(maestro):
    """position all leg joints at their initial positions"""

    for l in legs:
        m.set_speed(maestro, l[0], 20)
        m.set_speed(maestro, l[1], 20)
        m.set_speed(maestro, l[2], 20)

    
    for l, p in zip(legs, leg_zero_positions):
        m.set_target(maestro, l[0], p[0])
        time.sleep(0.2)
    
    while m.get_moving_state(maestro):
        pass
    
    for l, p in zip(legs, leg_zero_positions):
        time.sleep(0.2)
        m.set_target(maestro, l[1], p[1])

    while m.get_moving_state(maestro):
        pass

    for l, p in zip(legs, leg_zero_positions):
        m.set_target(maestro, l[2], p[2])
        time.sleep(0.2)

    while m.get_moving_state(maestro):
        pass

def lift_legs(maestro, leg_indices, pos):

    for i in leg_indices:
        m.set_target(maestro, legs[i][1], leg_zero_positions[i][1] + pos)
        
    while m.get_moving_state(maestro):
        pass

def lower_legs(maestro, leg_indices):

    for i in leg_indices:
        m.set_target(maestro, legs[i][1], leg_zero_positions[i][1])
        
    while m.get_moving_state(maestro):
        pass

def swing_legs(maestro, leg_indices, pos):

    for i in leg_indices:
        m.set_target(maestro, legs[i][0], leg_zero_positions[i][0] + pos)
        
    while m.get_moving_state(maestro):
        pass
    
    
def main():
    argv = sys.argv
    if len(argv) > 1:
        port = argv[1]
    else:
        port = '/dev/serial/by-id/usb-Pololu_Corporation_Pololu_Mini_Maestro_24-Channel_USB_Servo_Controller_00149355-if00'

    maestro = serial.Serial(port=port, baudrate=57600, timeout=1)
    init_legs(maestro)

    for i in range(3):
        lift_legs(maestro, [0, 2, 4], 1500)
        time.sleep(2.5)
        swing_legs(maestro, [0, 2, 4], 1500)
        swing_legs(maestro, [1, 3, 5], -1500)
        time.sleep(2.5)
        lower_legs(maestro, [0, 2, 4])
        time.sleep(2.5)
        lift_legs(maestro, [1, 3, 5], 1500)
        time.sleep(2.5)
        swing_legs(maestro, [1, 3, 5], 1500)
        swing_legs(maestro, [0, 2, 4], -1500)
        time.sleep(2.5)
        lower_legs(maestro, [1, 3, 5])
        time.sleep(2.5)
        
    

if __name__ == '__main__':
    main()
