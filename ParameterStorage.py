import datetime
from typing import Dict


__parameters = {}
__results = {}
__firstUse = True
__allMeasurements = {}

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
    global __results
    global __parameters
    if not paramName in __parameters.keys():
        print("Invalid parameter name")
        return None
    __results[paramName] = value  
    #print ("results: " + str(len(__results)) + " params: " + str(len(__parameters)))   
    if len(__results) == len(__parameters):
        print("Data added")
        __addToStack()

def __addToStack():
    global __allMeasurements
    global __results
    global lastFullParameters    
    #print("adding to stack")
    __allMeasurements[datetime.datetime.now()]= dict(__results)
    lastFullParameters = dict(__results)
    __results.clear()
    if len(__allMeasurements)>360:
        dumpMeasurements()

def __addCpuData():
    global __results
    __results["cpu load"] = "ff"

def dumpMeasurements():
    global __firstUse
    global __allMeasurements
    global __results
    saveStr = ""    
    if __firstUse:
        saveStr = "time;cpu load;cpu temp; gpu temp;"
        for s in __parameters:
            saveStr+= s + ";"
        saveStr+="\n"
        __firstUse=False
    for key in __allMeasurements.keys():
        saveStr+=str(key)+";"
        for s in __parameters:
            saveStr+=str(__allMeasurements[key][s])+";"
        saveStr+="\n"

    file = open("/windowManager/measurements.csv","a")    
    try:
        file.write(saveStr)
        __allMeasurements.clear()
        print("Data dumped")
    except:
        print("Write not possible")
    finally:
        file.close()
