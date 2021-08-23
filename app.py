from flask import Flask
from TheManager import TheManager
from WindowsController import isWindowOpen
from ParameterStorage import getLastParams
app = Flask(__name__)



@app.route("/")
def status():
    params = getLastParams()
    retVal = "Obecny status:<br>"
    keys = sorted(params.keys())    
    for s in keys:
        print(s)
        retVal += s +": " + str(params[s]) + "<br>"
    retVal += "Okno obecnie jest " + ("otwarte" if isWindowOpen() else "zamknięte") + ".<br>"
    print(retVal)
    return retVal


windowManager = TheManager()
windowManager.start()
if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')