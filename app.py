from flask.wrappers import Request
from Enums import isWindow, settingNames, settingType
from flask import Flask, render_template, redirect
from TheManager import TheManager
from ParameterStorage import getLastParams, getUnit
import conditions, math
from FormsSettings import SettingsForm

app = Flask(__name__)
app.config["SECRET_KEY"]="34fgsdg2aqsgf2938q248y7eb2WEGAQ23"

@app.route("/home")
@app.route("/")
def status():
    params = getLastParams()
    keys = sorted(params.keys())    
    newParams = []
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
                u =  "°C" if t==settingType.floatT else "ppm"
                val = f"{v:.2f}{u}"
        elif t==settingType.floatHr:
            d,i = math.modf(v)
            mins = d*60
            val = f"{int(i):02}:{int(mins):02}"
        newSettings.append({"name" : name, "value" : val})
    return render_template("settings.html", title = "Windows Commander - panel ustawień", params = newSettings)

@app.route("/settingsChange", methods=["POST","GET"])
def settingsChange():    
    form = SettingsForm()
    if form.validate_on_submit():
        conditions.manualOverride = form.manualOverride.data
        conditions.closeBelowThisTemp = float(conditions.getRidOfGarbage(form.closeBelowThisTemp.data))
        conditions.openAboveThisCO2 = float(conditions.getRidOfGarbage(form.openAboveThisCO2.data))
        conditions.weekdayClosingTime = conditions.convertStringToTimeFloat(form.weekdayClosingTime.data)
        conditions.weekendClosingTime = conditions.convertStringToTimeFloat(form.weekendClosingTime.data)
        conditions.weekdayOpeningTime = conditions.convertStringToTimeFloat(form.weekdayOpeningTime.data)
        conditions.weekendOpeningTime = conditions.convertStringToTimeFloat(form.weekendOpeningTime.data)
        conditions.saveSettings()
        return redirect("/settings")
    return render_template("settingsForm.html", title = "Windows Commander - panel ustawień", form = form)

windowManager = TheManager()
#windowManager.testing=True
windowManager.start()
if __name__ == '__main__':
    app.run(debug=windowManager.testing, port=80, host='0.0.0.0')