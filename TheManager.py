from WindowsController import *
from datetime import datetime
from time import sleep
import Display
import traceback
import conditions
from WhatToDoEnum import WhatToDo
from threading import Thread

counter = 0
class TheManager(Thread):
    disp = Display.Display(2,16)
    instance = counter
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
        try:    
            while True:
                nowFull = datetime.now()        
                toDo = conditions.canIclose(nowFull)
                if toDo == WhatToDo.open:
                    #pass
                    self.openWindow()
                elif toDo == WhatToDo.close:
                    self.closeWindow()
                self.disp.displayInLoop(nowFull)
                sleep(15)
                #sleep(2)
        except Exception as e:
            print(traceback.print_exc())
            self.disp.displayTextLine("Program się wywalił.",True,0,8)
            self.disp.displayTextLine("Zaloguj się na maszynę",False,8,8)
            self.disp.displayTextLine("i sprawdź trace'a",False,16,8)
        finally:
            #pass
            ParameterStorage.dumpMeasurements()





