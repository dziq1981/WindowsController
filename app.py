from flask import Flask
from TheManager import TheManager
from WindowsController import isWindowOpen
app = Flask(__name__)



@app.route("/")
def status():
    str = "Obecny status:<br>"
    str += "Okno obecnie jest " + ("otwarte" if isWindowOpen() else "zamknięte") + ".<br>"
    return str


windowManager = TheManager()
windowManager.start()
if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')