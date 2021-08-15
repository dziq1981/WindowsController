from WindowsController import *
from datetime import datetime
from time import sleep
import sys
import Display
import traceback
import ParameterStorage


disp = Display.Display(2,16)
controllerTurnRelaysOff()

def convertTimeToFloat(hrs, min):    
    return float(hrs)+float(min)/60.0

def openWindow():
    #global windowOpenedFlag
    disp.displayTextLine("Otwieram okno!",True,2)
    print("Opening the window")
    #windowOpenedFlag = True
    controllerOpenWindow()

def closeWindow():
    #global windowOpenedFlag
    disp.displayTextLine("Zamykam okno!",True,2)
    print("Closing the window")
    #windowOpenedFlag = False
    controllerCloseWindow()



closingTime = convertTimeToFloat(23,00)
openingTime = convertTimeToFloat(6,0)

if closingTime<openingTime:
    print("At the moment the window has to be opened earlier than being closed")
    sys.exit()

firstTime = True
#windowOpenedFlag = False

try:    
    while True:
        nowFull = datetime.now()        
        now = convertTimeToFloat(nowFull.hour,nowFull.minute)
        #text= str(nowFull.hour) +":" + ("0" if nowFull.minute<10 else "") + "{:02d}".format(str(nowFull.minute))        
        if firstTime:
            if now>=openingTime and now<closingTime:
                openWindow()                
            else:
                closeWindow()
            firstTime = False
        else:
            if now>=openingTime and now<closingTime and not isWindowOpen(): #windowOpenedFlag:
                openWindow()                
            elif now>=closingTime and isWindowOpen():#windowOpenedFlag:
                closeWindow()
        disp.displayInLoop(nowFull)
        sleep(15)
except Exception as e:
    print(traceback.print_exc())
    disp.displayTextLine("Program się wywalił.",True,0,8)
    disp.displayTextLine("Zaloguj się na maszynę",False,8,8)
    disp.displayTextLine("i sprawdź trace'a",False,16,8)
finally:
    ParameterStorage.dumpMeasurements()





