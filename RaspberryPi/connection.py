#!/usr/bin/env python3
import serial

if __name__ == '__main__':
<<<<<<< HEAD
    ser1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser2 = serial.Serial('/dev/rfcomm0')
    ser1.flush()

    while True:
        #Communication from Arduino to Pi
        if ser1.in_waiting > 0:
            arduino = ser1.readline().decode('utf-8').rstrip()
            #print(arduino)
        #Communication from Phone to Pi
        if ser2.in_waiting > 0:
            phone = ser2.readline().decode('utf-8').rstrip()
            #print(phone)
        

        
=======
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #Set the serial port to be ttyUSB0 at a baudrate of 9600
    ser.flush() #Wait till data is written

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('latin-1').rstrip() #Read
            print(line)
>>>>>>> 958469a4f4c04b9074539a3b53f49bc556463e9f
