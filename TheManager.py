from tkinter import E
import WindowsController 
from datetime import datetime
from time import sleep
import Display
import traceback
import conditions
import ParameterStorage
from Enums import whatToDo
from threading import Thread
from Enums import isWindow

counter = 0
class TheManager(Thread):
    disp = Display.Display(2,16)
    instance = counter
    testing = False
    WindowsController.controllerTurnRelaysOff()
    markerDirectory = "/windowManager/marker/"

    def createMarker(self, state: isWindow):        
        name = ""
        name += self.markerDirectory
        if state == isWindow.open:
            name+="open"
        elif state == isWindow.close:
            name+="close"
        else:
            return
        name+=str(datetime.timestamp(datetime.now()))
        print(name)
        try:
            open(name, mode='a')
        except OSError:
            print("Marker creation failed")


    def openWindow(self):
        self.disp.displayTextLine("Otwieram okno!",True,2)
        print("Opening the window")
        WindowsController.controllerOpenWindow()
        self.createMarker(isWindow.open)
        

    def closeWindow(self):    
        self.disp.displayTextLine("Zamykam okno!",True,2)
        print("Closing the window")
        WindowsController.controllerCloseWindow()
        self.createMarker(isWindow.close)

    def run(self) -> None: 
        global counter
        counter +=1
        if self.instance>0:
            print("Unnecesary invocation of TheManager")
            return None

        iterationCount=0
        displayDelay = 2 if self.testing else 2
        try:                
            while True:
                iterationCount+=1
                nowFull = datetime.now() 
                if self.testing:
                    WindowsController.isWindowOpen()
                toDo = whatToDo.doNothing if self.testing else conditions.canIclose(nowFull)                
                if toDo == whatToDo.open:
                    self.openWindow()
                elif toDo == whatToDo.close:
                    self.closeWindow()                
                if iterationCount>=displayDelay:                    
                    iterationCount=0
                    try:
                        self.disp.displayInLoop(nowFull)
                    except Exception as ex:
                        print(traceback.print_exc())        
                sleep(2)
                #sleep(2)
        except Exception as e:
            print(traceback.print_exc())
            self.disp.displayTextLine("Program się wywalił.",True,0,8)
            self.disp.displayTextLine("Zaloguj się na maszynę",False,8,8)
            self.disp.displayTextLine("i sprawdź trace'a",False,16,8)
        finally:
            #pass
            if not self.testing:
                ParameterStorage.dumpMeasurements()





