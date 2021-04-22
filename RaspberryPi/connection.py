#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser2 = serial.Serial('/dev/rfcomm0')
    ser1.flush()
    ser2.flush()
    phone = ""
    arduinio = ""
    mode = 1 # 1 = Brake 0 = Coast
    while True:
        #Communication from Arduino to Pi
        if ser1.in_waiting > 0:
            arduino = ser1.readline().decode('utf-8').rstrip()
            #print(arduino)
        #Communication from Phone to Pi
        if ser2.in_waiting > 0:
            phone = ser2.readline().decode('utf-8').rstrip()
            #print(phone)
        if phone == "Exit":
            quit()
        elif phone == "Coast":
            mode = 0
        else:
            mode = 1


        
