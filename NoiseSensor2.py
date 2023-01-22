#NoiseSensor2
from time import sleep
import RPi.GPIO as GPIO

pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)
while True:
    if GPIO.input(pin) == 0:
        print("klap")            
        sleep(1)
    else:
        print("nie klap")
    
    