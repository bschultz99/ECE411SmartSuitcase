#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #Set the serial port to be ttyUSB0 at a baudrate of 9600
    ser.flush() #Wait till data is written

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('latin-1').rstrip() #Read
            print(line)