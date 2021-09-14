import serial
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LPGdetect = 23
GPIO.setup(LPGdetect, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
xbee = serial.Serial()
xbee.port = "/dev/ttyAMA0"
xbee.baudrate = 9600
xbee.timeout = 1
xbee.writeTimeout = 1

if xbee.is_open == False:
    xbee.open()
print("Port open status: ", xbee.is_open)
print("Receive & Transfer start")

while True:
    try:
        data = xbee.readline().strip()
        alertflag = GPIO.input(LPGdetect)

        if data == b'LPG':
            print("Receive: {0} status required".format(data))
            if alertflag == 1:
                xbee.write(b'LPGWARN')
                print('LPGWARN')
            elif alertflag == 0:
                xbee.write(b'LPGOK')
                print('LPGOK')
            
    except KeyboardInterrupt:
        break
    time.sleep(0.1)

xbee.close()
GPIO.cleanup()