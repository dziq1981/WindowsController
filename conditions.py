from os import close
from time import sleep
import WindowsController
import datetime
import TemperatureSensor
from Enums import whatToDo, isWindow, settingNames, settingType
import threading

def convertTimeToFloat(hrs, min):    
    return float(hrs)+float(min)/60.0

def convertStringToTimeFloat(timeString):
    strFromParam = getRidOfGarbage(timeString)
    strList = strFromParam.split(":")
    print (f"1. {strList[0]} and 2. {strList[1]}")
    hrs = float(strList[0])
    mins = float(strList[1])/60.0
    return hrs+mins

def getRidOfGarbage(timeString):
    print(timeString)
    strFromParam = str(timeString)
    strFromParam= strFromParam.replace("[","")
    strFromParam= strFromParam.replace("]","")
    strFromParam= strFromParam.replace("'","")
    return strFromParam

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

def canIclose(now) -> whatToDo:    
    global firstTime, userClosingTrigger, userOpeningTrigger, manualOverride, lastSensorRead,tooCold,tooHumid, tickTack
    nowf = convertTimeToFloat(now.hour,now.minute)
    isItWeekday = datetime.datetime.now().isoweekday()<=5
    if (now>lastSensorRead+datetime.timedelta(minutes=1) or firstTime): #read it no frequent than once per minute - those changes are not that rapid
        tooCold = sensor.readTemp()<closeBelowThisTemp
        tooHumid = False #sensor.readHumidity()>openAboveThisHumidity
        lastSensorRead = now
    if firstTime and WindowsController.isWindowOpen() != isWindow.unknown:
        firstTime = False

    if firstTime:
        firstTime=False
        return closeCondition(nowf, weekdayOpeningTime if isItWeekday else weekendOpeningTime,
        weekdayClosingTime if isItWeekday else weekendClosingTime)

    isWindowOpen = WindowsController.isWindowOpen()==isWindow.open
    
    if isWindowOpen and userClosingTrigger:
        userClosingTrigger = False
        manualOverride = True
        return whatToDo.close

    if not isWindowOpen and userOpeningTrigger:
        userOpeningTrigger = False
        manualOverride = True
        return whatToDo.open

    if tickTack.running:
        return whatToDo.doNothing

    if not manualOverride:
        if isWindowOpen and tooCold:
            if not tickTack.running:
                tickTack= Ticker()
                tickTack.start()
            return whatToDo.close
        elif not isWindowOpen and tooCold:
            if not tickTack.running:
                tickTack= Ticker()
                tickTack.start()
            return whatToDo.doNothing
        #elif not isWindowOpen and tooHumid:
        #    if not tickTack.running:
        #        tickTack= Ticker()
        #        tickTack.start()
        #    return whatToDo.open
    
    retVal = closeCondition(nowf, weekdayOpeningTime if isItWeekday else weekendOpeningTime,
        weekdayClosingTime if isItWeekday else weekendClosingTime)
    if retVal==whatToDo.close:
        if not isWindowOpen:
            manualOverride = False
            retVal = whatToDo.doNothing
        elif manualOverride:
            retVal = whatToDo.doNothing
    elif retVal==whatToDo.open:
        if isWindowOpen:
            manualOverride = False
            retVal = whatToDo.doNothing
        elif manualOverride:
            retVal = whatToDo.doNothing

    return retVal

def closeCondition(nowf, openingTime, closingTime)->whatToDo:
    global tooHumid,tooCold
    closingTime = nowf<openingTime or nowf>closingTime
    tempHumidCondition = bool
    if tooCold:
        tempHumidCondition = True
    #elif tooHumid:
    #    tempHumidCondition = False
    return whatToDo.close if closingTime and tempHumidCondition else whatToDo.open

def getSettings():
    global manualOverride, weekendOpeningTime, weekendClosingTime, weekdayClosingTime, weekdayOpeningTime, closeBelowThisTemp, openAboveThisHumidity    
    item00 = __generateSetting(settingNames.manualOverride.value, manualOverride, settingType.bool)
    item01 = __generateSetting(settingNames.weekendOpeningTime.value,weekendOpeningTime, settingType.floatHr)
    item02 = __generateSetting(settingNames.weekendClosingTime.value,weekendClosingTime, settingType.floatHr)
    item03 = __generateSetting(settingNames.weekdayOpeningTime.value,weekdayOpeningTime, settingType.floatHr)
    item04 = __generateSetting(settingNames.weekdayClosingTime.value,weekendClosingTime, settingType.floatHr)
    item05 = __generateSetting(settingNames.closeBelowThisTemp.value,closeBelowThisTemp, settingType.floatT)
    item06 = __generateSetting(settingNames.openAboveThisHumidity.value,openAboveThisHumidity, settingType.floatH)
    return [item00,item01,item02,item03,item04,item05,item06]
    

def __generateSetting(name, value, type):    
    return { "name": name, "value": value, "type": type}

def setSettings(settings):
    global manualOverride, weekendOpeningTime, weekendClosingTime, weekdayClosingTime, weekdayOpeningTime, closeBelowThisTemp, openAboveThisHumidity    
    for setting in settings:
        n = setting["name"]
        v = setting["value"]
        if n==settingNames.manualOverride.value:
            manualOverride = v=="True"
            print(f"Setting {n} to {v}")
        elif n==settingNames.weekendOpeningTime.value:
            weekendOpeningTime = float(v)
            print(f"Setting {n} to {v}")
        elif n==settingNames.weekendClosingTime.value:            
            weekendClosingTime = float(v)
            print(f"Setting {n} to {v}")
        elif n==settingNames.weekdayOpeningTime.value:
            weekdayOpeningTime = float(v)
            print(f"Setting {n} to {v}")
        elif n==settingNames.weekdayClosingTime.value:
            weekdayClosingTime = float(v)
            print(f"Setting {n} to {v}")
        elif n==settingNames.closeBelowThisTemp.value:
            closeBelowThisTemp = float(v)
            print(f"Setting {n} to {v}")
        elif n==settingNames.openAboveThisHumidity.value:
            openAboveThisHumidity = float(v)
            print(f"Setting {n} to {v}")        

def saveSettings():
    file = open("settings.cfg","w+t")
    strng = ""
    for setting in getSettings():
        strng+=setting["name"] + "=" + str(setting["value"])+"\n"
    try:      
        file.write(strng)
    finally:
        file.close()

def loadSettings():
    file = open("settings.cfg","r+t")
    strng = []
    settings = []
    try:
        strng = file.readlines()
    finally:
        file.close()
    for s in strng:
        ss=s.replace("\n","").split("=")        
        settings.append(__generateSetting(ss[0],ss[1],None))
    setSettings(settings)


firstTime = True
manualOverride = False

weekdayOpeningTime=6.0
weekdayClosingTime=23.0

weekendOpeningTime = 8.0
weekendClosingTime = 23.0

closeBelowThisTemp = 10.0
openAboveThisHumidity = 90.0

userClosingTrigger = False
userOpeningTrigger = False

tickTack = Ticker()
sensor = TemperatureSensor.Si7021()
tickTack.sleepTime=1800
lastSensorRead = datetime.datetime.now()
tooCold = False
tooHumid = False

loadSettings()
