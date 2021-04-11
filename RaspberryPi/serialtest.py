from serial import Serial
if __name__ == "__main__":
    ser=Serial("/dev/ttyUSB0",9600) 
    ser.flushInput()
    while True:
        ser.write(1)
        
print("done")
