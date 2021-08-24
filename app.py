from flask.wrappers import Request
from Enums import isWindow
from flask import Flask, render_template
from TheManager import TheManager
#from WindowsController import isWindowOpen
from ParameterStorage import getLastParams, getUnit
import conditions
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
    #    retVal += s +": " + str(params[s]) + "<br>"
    #retVal += "Okno obecnie jest " + ("otwarte" if isWindowOpen() else "zamknięte") + ".<br>"
    #print(retVal)
    return render_template("home.html", title = "Window Manager Status Page", params = newParams)

@app.route("/open")
def openWindow():
    conditions.userOpeningTrigger = True
    print("User opening")
    return status()

@app.route("/close")
def closeWindow():
    conditions.userClosingTrigger = True
    print("User closing")
    return status()


windowManager = TheManager()
#windowManager.testing=True
windowManager.start()
if __name__ == '__main__':
    app.run(debug=windowManager.testing, port=80, host='0.0.0.0')