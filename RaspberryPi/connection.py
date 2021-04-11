#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('latin-1').rstrip()
            print(line)