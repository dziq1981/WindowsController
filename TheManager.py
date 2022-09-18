from WindowsController import *
from datetime import datetime
from time import sleep
import Display
import traceback
import conditions
from Enums import whatToDo
from threading import Thread

counter = 0
class TheManager(Thread):
    disp = Display.Display(2,16)
    instance = counter
    testing = False
    controllerTurnRelaysOff()

    def openWindow(self):
        self.disp.displayTextLine("Otwieram okno!",True,2)
        print("Opening the window")
        controllerOpenWindow()

    def closeWindow(self):    
        self.disp.displayTextLine("Zamykam okno!",True,2)
        print("Closing the window")
        controllerCloseWindow()

    def run(self) -> None: 
        global counter
        counter +=1
        if self.instance>0:
            print("Unnecesary invocation of TheManager")
            return None

        iterationCount=0
        displayDelay = 2 if self.testing else 5
        try:                
            while True:
                iterationCount+=1
                nowFull = datetime.now() 
                if self.testing:
                    isWindowOpen()       
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





