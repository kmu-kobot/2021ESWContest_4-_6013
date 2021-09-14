import serial
import time
import RPi.GPIO as GPIO
import re
GPIO.setmode(GPIO.BCM)
xbee = serial.Serial()
xbee.port = "/dev/ttyAMA1"
xbee.baudrate = 9600
xbee.timeout = 1
xbee.writeTimeout = 1

if xbee.is_open == False:
    xbee.open()
print("Port open status: ", xbee.is_open)
print("Receive & Transfer start")

def Receive():
    xbee.flushInput()
    rsByte= xbee.readline().strip()
    print(rsByte)

    return rsByte

def Transfer(data):
    if type(data) == type(b''):
        xbee.write(data)
    else:
        data = re.sub('\n', '', data)
        tsData = bytes(data, 'utf-8')
        xbee.write(tsData)
while True:
    try:
        print("Please type the device to check (LPG / CO / EXIT) :")
        tsString = input()
        if tsString == "LPG":
            Transfer(tsString)
            time.sleep(0.1)
            rsByte = Receive()
            if rsByte == b'LPGOK':
                print("LPG status is OK") 
                #Need to fill below (Communicate with mobile server)
            elif rsByte == b'LPGWARN':
                print("LPG WARNING")
                #Need to fill below (In LPG warning situation, what have to do)
        
        elif tsString == "CO":
            Transfer(tsString)
            rsByte = Receive()
            rsString = rsByte.decode('utf-8')

            if rsString == "WARNING":
                COstat_Byte = Receive()
                time.sleep(0.01)
                COstat = int(COstat_Byte.decode('utf-8'))
                print("COstat = {0}\n".format(COstat))
                #Need to fill below (Communicate with mobile server)

            else:
                COstat = int(rsString)
                print("COstat = {0}\n".format(COstat))
                #Need to fill below (In CO warning situation, what have to do)
        elif tsString == "EXIT":
            break
        else:
            print("Please Input the correct command")
            continue

    except KeyboardInterrupt:
        break
    time.sleep(0.1)

xbee.close()
#GPIO.cleanup()