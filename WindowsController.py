from gpiozero import OutputDevice
from time import sleep
import ParameterStorage
from Enums import isWindow
from glob import glob
from os import path
import TheManager
import sys

relay1 = OutputDevice(6) #relay hooked on pin 6 - note that the relay is activated with a LOW SIGNAL (off)
relay2 = OutputDevice(5) #relay hooked on pin 5 - note that the relay is activated with a LOW SIGNAL (off)
duration = 15 #how long should relays be switched on during opening/closing


WINDOW_OPEN_PARAM_NAME = "Okno"
ParameterStorage.addParameter(WINDOW_OPEN_PARAM_NAME,"")
__isWindowOpen = isWindow.unknown

def readMarker()-> isWindow:    
    try:        
        list_of_files = glob(TheManager.TheManager.markerDirectory+"*")
        latest_file = max(list_of_files, key=path.getctime)
        print(latest_file)
        if latest_file.find("open")>0:
            print("I think the window is currently OPEN")
            return isWindow.open
        elif latest_file.find("close")>0:
            print("I think the window is currently CLOSED")
            return isWindow.close
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return isWindow.unknown
        


def isWindowOpen():
    global __isWindowOpen
    if __isWindowOpen==isWindow.unknown:
        __isWindowOpen=readMarker()
    ParameterStorage.provideValue(WINDOW_OPEN_PARAM_NAME,__isWindowOpen)
    return __isWindowOpen


def controllerOpenWindow():
    global relay1
    global relay2
    global duration
    global __isWindowOpen
    print("Open")
    try:
        relay2.off()
        relay1.on()
        sleep(duration-2)
        __isWindowOpen=isWindow.open
    finally:
        controllerTurnRelaysOff()

def controllerCloseWindow():
    global relay1
    global relay2
    global duration
    global __isWindowOpen
    print("Close")
    try:
        relay1.off()
        relay2.on()
        sleep(duration)
        __isWindowOpen=isWindow.close
    finally:
        controllerTurnRelaysOff()

def controllerTurnRelaysOff():
    global relay1
    global relay2
    print("Relays off")
    try: #to turn the relay off you nedd to set the corresponding signal high
        relay2.on()
        relay1.on()
    except:
        print("That went wrong in closing relays...")

        