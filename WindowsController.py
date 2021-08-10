from gpiozero import OutputDevice
from time import sleep

relay1 = OutputDevice(6) #relay hooked on pin 6 - note that the relay is activated with a LOW SIGNAL (off)
relay2 = OutputDevice(5) #relay hooked on pin 5 - note that the relay is activated with a LOW SIGNAL (off)
duration = 15 #how long should relays be switched on during opening/closing

def controllerOpenWindow():
    global relay1
    global relay2
    global duration
    print("Open")
    try:
        relay2.off()
        relay1.on()
        sleep(duration)
    finally:
        controllerTurnRelaysOff()
def controllerCloseWindow():
    global relay1
    global relay2
    global duration
    print("Close")
    try:
        relay1.off()
        relay2.on()
        sleep(duration)
    finally:
        controllerTurnRelaysOff()

def controllerTurnRelaysOff():
    global relay1
    global relay2
    print("Relays off")
    try: #to turn the relay off you nedd to set the corresponding signal high
        relay2.on()
        relay1.on()
    except:
        print("That went wrong in closing relays...")

        