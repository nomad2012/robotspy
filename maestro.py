#!/usr/bin/env python
"""maestro.py - commands and queries for a Pololu mini-maestro servo controller
"""

import serial
import string
import struct
import sys


def set_target(port, channel, target):
    """set target position for servo channel on port.
    target is in units of 0.25us, e.g. a value of 6000 = 1500us"""
    port.write(stuct.pack('BBBB', 0x84, channel, target & 0x7f, (target >> 7) & 0x7f))

def set_targets(port, first_channel, targets):
    """set multiple targets starting at first_channel to the values in targets on port.
    targets are in units of 0.25us, e.g. a value of 6000 = 1500us"""
    cmd = struct.pack('BBB', 0x9F, len(targets), first_channel)
    for t in targets:
        cmd += struct.pack('BB', t & 0x7f, (t >> 7) & 0x7f)
    port.write(cmd)

def set_speed(port, channel, speed):
    """set target speed for servo channel on port.
    speed is in units of (0.25us/10ms)"""
    
    port.write(struct.pack('BBBB', 0x87, channel, speed & 0x7f, (speed >> 7) & 0x7f))

def set_acceleration(port, channel, accel):
    """set target acceleration for servo channel on port.
    accel is in units of (0.25us/10ms/80ms)"""
    port.write(struct.pack('BBBB', 0x89, channel, accel & 0x7f, (accel >> 7) & 0x7f))

def set_pwm(port, on_time, period):
    """set the PWM output to on_time and period, in units of 1/48us"""
    port.write(struct.pack('BBBBB', 0x8A, on_time & 0x7f, (on_time >> 7) & 0x7f,
                           period & 0x7f, (period >> 7) & 0x7f))

def get_position(port, channel):
    """return the current position of servo channel on port"""
    port.write(struct.pack('BB', 0x90, channel))
    response = port.read(2)
    return struct.unpack('<H', response)

def get_moving_state(port):
    """return True if any servo is moving on port"""
    port.write(struct.pack('B', 0x93))
    response = port.read(1)
    return struct.unpack('B', response) == 1

def get_errors(port):
    """return the error bits (1 word) on port"""
    port.write(struct.pack('B', 0xA1))
    response = port.read(2)
    return struct.unpack('<H', response)
