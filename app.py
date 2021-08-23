from flask import Flask, render_template
from TheManager import TheManager
from WindowsController import isWindowOpen
from ParameterStorage import getLastParams
app = Flask(__name__)


@app.route("/home")
@app.route("/")
def status():
    params = getLastParams()
    #retVal = "Obecny status:<br>"
    keys = sorted(params.keys())    
    #for s in keys:
    #    print(s)
    #    retVal += s +": " + str(params[s]) + "<br>"
    #retVal += "Okno obecnie jest " + ("otwarte" if isWindowOpen() else "zamknięte") + ".<br>"
    #print(retVal)
    return render_template("home.html", title = "Window Manager Status Page", params = params, keys=keys)


windowManager = TheManager()
windowManager.testing=True
windowManager.start()
if __name__ == '__main__':
    app.run(debug=windowManager.testing, port=80, host='0.0.0.0')