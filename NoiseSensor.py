#from gpiozero import Button
from time import sleep
import threading
import RPi.GPIO as GPIO

pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)

class NoiseSensor(threading.Thread):
    isFirstClap = False
    #sensor = Button(26)
    isListening = True
    global pin
    def run(self):
        self.isFirstClap = False
        self.isListening = True
        #self.sensor = Button(26)
        while (self.isListening):
            #if self.sensor.is_pressed:
            if GPIO.input(26) == 0:
                print("klap")
                isFirstClap = True
                sleep(10)
            else:
                print("nie klap")
                isFirstClap = False
print("test")
obj = NoiseSensor
obj.start
clapCounter=0
while clapCounter<5:
    if obj.isFirstClap:
        print("1 klap")
        clapCounter+=1
print("koniec testu")