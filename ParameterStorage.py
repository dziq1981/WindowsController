import datetime
from typing import Dict


parameters = []
results = {}
firstUse = True
allMeasurements = {}




def addParameter(paramName):
    global parameters
    parameters.append(paramName)

def provideValue(paramName,value):
    global results
    global parameters
    if not paramName in parameters:
        print("Invalid parameter name")
        return None
    results[paramName] = value     
    if len(results) == len(parameters):
        addToStack()

def addToStack():
    global allMeasurements
    global results
    allMeasurements[datetime.datetime.now()]= dict(results)    
    results.clear()
    if len(allMeasurements)>120:
        dumpMeasurements()

def addCpuData():
    global results
    results["cpu load"] = "ff"

def dumpMeasurements():
    global firstUse
    global allMeasurements
    global results
    saveStr = ""    
    if firstUse:
        saveStr = "time;cpu load;cpu temp; gpu temp;"
        for s in parameters:
            saveStr+= s + ";"
        saveStr+="\n"
        firstUse=False
    for key in allMeasurements.keys():
        saveStr+=str(key)+";"
        for s in parameters:
            saveStr+=str(allMeasurements[key][s])+";"
        saveStr+="\n"

    file = open("/windowManager/measurements.csv","a")    
    try:
        file.write(saveStr)
        allMeasurements.clear()
        print("Data dumped")
    except:
        print("Write not possible")
    finally:
        file.close()
