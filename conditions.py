from os import close
from time import sleep
import WindowsController
import datetime
import TemperatureSensor
from Enums import WhatToDo, isWindow
import threading

firstTime = True
manualOverride = False

weekdayOpeningTime=6.0
weekdayClosingTime=23.0

weekendOpeningTime = 8.0
weekendClosingTime = 23.0

closeBelowThisTemp = 10.0
openAboveThisHumidity = 80.0

userClosingTrigger = False
userOpeningTrigger = False

def convertTimeToFloat(hrs, min):    
    return float(hrs)+float(min)/60.0

class Ticker(threading.Thread):
    running = False   
    sleepTime = 1800  
    """sleep time in seconds"""
    def run(self) -> None:
        self.running = True
        startTime = datetime.datetime.now()
        endTime = startTime + datetime.timedelta(seconds=self.sleepTime)
        currentTime = startTime
        while currentTime<endTime:
            sleep(10)
            currentTime=datetime.datetime.now()
        self.running = False        

tickTack = Ticker()
sensor = TemperatureSensor.Si7021()
tickTack.sleepTime=1800

def canIclose(now) -> WhatToDo:    
    global firstTime, userClosingTrigger, userOpeningTrigger, manualOverride    
    nowf = convertTimeToFloat(now.hour,now.minute)
    isItWeekday = datetime.datetime.now().isoweekday()<=5
    tooCold = sensor.readTemp()<closeBelowThisTemp
    tooHumid = sensor.readHumidity()>openAboveThisHumidity
    if firstTime:
        firstTime=False
        if isItWeekday:            
            return WhatToDo.close if (nowf<weekdayOpeningTime or nowf>weekdayClosingTime or tooCold) and not tooHumid else WhatToDo.open
        else:
            return WhatToDo.close if (nowf<weekendOpeningTime or nowf>weekendClosingTime or tooCold) and not tooHumid else WhatToDo.open

    isWindowOpen = WindowsController.isWindowOpen()==isWindow.open
    
    if isWindowOpen and userClosingTrigger:
        userClosingTrigger = False
        manualOverride = True
        return WhatToDo.close
    if not isWindowOpen and userOpeningTrigger:
        userOpeningTrigger = False
        manualOverride = True
        return WhatToDo.open

    if tickTack.running:
        return WhatToDo.doNothing

    if not manualOverride:
        if isWindowOpen and tooCold:
            tickTack.run()
            return WhatToDo.close
        elif not isWindowOpen and tooCold:
            tickTack.run()
            return WhatToDo.doNothing
        elif not isWindowOpen and tooHumid:
            tickTack.run()
            return WhatToDo.open
    
    retVal = WhatToDo.doNothing


    retVal = (WhatToDo.close if (timeToClose(nowf, weekdayOpeningTime if isItWeekday else weekendOpeningTime,
        weekdayClosingTime if isItWeekday else weekendClosingTime) or tooCold) and not tooHumid else WhatToDo.open)
    if retVal==WhatToDo.close:
        if not isWindowOpen:
            manualOverride = False
            retVal = WhatToDo.doNothing
        elif manualOverride:
            retVal = WhatToDo.doNothing
    elif retVal==WhatToDo.open:
        if isWindowOpen:
            manualOverride = False
            retVal = WhatToDo.doNothing
        elif manualOverride:
            retVal = WhatToDo.doNothing

    return retVal

def timeToClose(nowf, openingTime, closingTime)->bool:
    return nowf<openingTime or nowf>closingTime