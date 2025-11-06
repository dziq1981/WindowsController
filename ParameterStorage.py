import datetime
import time
import os.path
from typing import Dict


__parameters = {}
__results = {}
__firstUse = True
__allMeasurements = {}
__counter = 0
lastFullParameters = {}


def getLastParams() -> dict():
    global lastFullParameters
    return lastFullParameters

def addParameter(paramName, paramUnit):
    global __parameters
    if not paramName in __parameters.keys():
        #print("+++++ PARAMETER " + paramName + "ADDED+++++")
        __parameters[paramName]=paramUnit

def getUnit(paramName) ->str:
    global __parameters
    return __parameters[paramName]

def provideValue(paramName,value):
    global __results, __parameters, __counter
    if not paramName in __parameters.keys():
        print("Invalid parameter name")
        return None
    __results[paramName] = value  
    #print ("results: " + str(len(__results)) + " params: " + str(len(__parameters)))   
    if len(__results) == len(__parameters):        
        __counter+=1
        if (__counter>=25):
            __counter=0
            print(str(time.time())+"Data added")
            __addToStack()

def __addToStack():
    global __allMeasurements
    global __results
    global lastFullParameters    
    #print("adding to stack")
    __allMeasurements[datetime.datetime.now()]= dict(__results)
    lastFullParameters = dict(__results)
    __results.clear()
    if len(__allMeasurements)>75:
        dumpMeasurements()

def __addCpuData():
    global __results
    __results["cpu load"] = "ff"

def dumpMeasurements():
    global __firstUse
    global __allMeasurements
    global __results
    saveStr = ""    
    filePath = "/windowManager/measurements.csv"
    __firstUse = not os.path.isfile(filePath)
    if __firstUse:
        saveStr = "time;" #"time;cpu load;cpu temp; gpu temp;"
        for s in __parameters:
            saveStr+= s + ";"
        saveStr+="\n"
        __firstUse=False
    for key in __allMeasurements.keys():
        saveStr+=str(key)+";"
        for s in __parameters:
            saveStr+=str(__allMeasurements[key][s])+";"
        saveStr+="\n"
    
    file = open(filePath,"a")    
    try:
        file.write(saveStr)
        __allMeasurements.clear()
        print("Data dumped")
    except:
        print("Write not possible")
    finally:
        file.close()
