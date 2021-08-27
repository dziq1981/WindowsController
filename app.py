from flask.wrappers import Request
from Enums import isWindow, settingNames, settingType
from flask import Flask, render_template, redirect
from TheManager import TheManager
#from WindowsController import isWindowOpen
from ParameterStorage import getLastParams, getUnit
import conditions, math
app = Flask(__name__)


@app.route("/home")
@app.route("/")
def status():
    params = getLastParams()
    keys = sorted(params.keys())    
    newParams = []
    print(type(0.01))
    for key in keys:        
        k = str(key)
        v = params[key]
        val = str
        if type(v) is isWindow:
            if v==isWindow.open:
                    val = "otwarte"
            elif v==isWindow.close:
                val = "zamknięte"
            else:
                val = "nieokreślone"
        else:
            val = f"{v:.2f}" if type(v) is float else str(v)
        singleParam = {
            'name': k,             
            'value' : val,
            'unit' : getUnit(k)
            }
        newParams.append(singleParam)        
    return render_template("home.html", title = "Windows Commander - panel statusu", params = newParams)

@app.route("/open")
def openWindow():
    conditions.userOpeningTrigger = True
    print("User opening")
    return redirect("/")

@app.route("/close")
def closeWindow():
    conditions.userClosingTrigger = True
    print("User closing")    
    return redirect("/")

@app.route("/settings")
def settings():    
    print("Settings") 
    settings = conditions.getSettings()   
    newSettings=[]
    for setting in settings:
        name = str(setting["name"])
        v = setting["value"]
        t = setting["type"]
        val = str
        if t==settingType.bool:
            val = "Włączone" if v else "Wyłączone"
        elif t==settingType.floatH or t==settingType.floatT:
                u =  "°C" if t==settingType.floatT else "%"
                val = f"{v:.2f}{u}"
        elif t==settingType.floatHr:
            d,i = math.modf(v)
            mins = d*60
            val = f"{int(i):02}:{int(mins):02}"
        newSettings.append({"name" : name, "value" : val})
    return render_template("settings.html", title = "Windows Commander - panel ustawień", params = newSettings)

windowManager = TheManager()
#windowManager.testing=True
windowManager.start()
if __name__ == '__main__':
    app.run(debug=windowManager.testing, port=80, host='0.0.0.0')