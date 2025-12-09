import scd4x_rpi
import ParameterStorage
import time

def singleton(cls):
    """
    Dekorator, który przekształca klasę w Singleton.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class SCD41Middleware:

    readyCounter:int = 0
    resetWhenCounterIsAbove:int = 50
    lastTemperature:float = 0.0
    lastHumidity:float = 0.0
    lastCO2:int = 0
    reseting:bool = False
    sensor:scd4x_rpi.SCD4X_RPI = None
    TEMPERATURE_PARAM_NAME = "Temperatura"
    RELATIVE_HUMIDITY_PARAM_NAME = "Wilgotność"
    CO2_PARAM_NAME = "Stężenie CO2"

    def __init__(self):
        self.sensor = scd4x_rpi.SCD4X_RPI()
        self.restart()
        ParameterStorage.addParameter(self.TEMPERATURE_PARAM_NAME,"°C")
        ParameterStorage.addParameter(self.RELATIVE_HUMIDITY_PARAM_NAME,"%")
        ParameterStorage.addParameter(self.CO2_PARAM_NAME,"ppm")

    def start(self):
        self.sensor.start_periodic_measurement()
        time.sleep(5)  # Poczekaj 5 sekund na pierwsze dane pomiarowe

    def stop(self):
        self.sensor.stop_periodic_measurement()

    def values(self):        
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
            self.readyCounter=0
            self.lastTemperature = self.sensor.temperature
            self.lastHumidity = self.sensor.humidity
            self.lastCO2 = self.sensor.co2
        else:
            self.readyCounter+=1
            if self.readyCounter>50 and not self.reseting:
                self.restart()
        ParameterStorage.provideValue(self.TEMPERATURE_PARAM_NAME,self.sensor.temperature)        
        ParameterStorage.provideValue(self.RELATIVE_HUMIDITY_PARAM_NAME,self.sensor.humidity)        
        ParameterStorage.provideValue(self.CO2_PARAM_NAME,self.sensor.co2)
        return self.sensor.temperature, self.sensor.humidity, self.sensor.co2

    def restart(self):
        print("Restarting SCD41 sensor...")
        self.reseting = True
        try:
            self.stop()
            time.sleep(10)
            self.start()
            self.readyCounter = 0
            self.lastTemperature = 0.0
            self.lastHumidity = 0.0
            self.lastCO2 = 0
        finally:
            self.reseting = False
            print("SCD41 sensor restarted.")
        

    def temperature(self):
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
            self.readyCounter=0
        else:
            self.readyCounter+=1
            if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
                self.restart()
        return self.sensor.temperature
    
    def humidity(self):
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
            self.readyCounter=0
        else:
            self.readyCounter+=1
            if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
                self.restart()
        return self.sensor.humidity
    
    def co2(self):        
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
            self.readyCounter=0
        else:
            self.readyCounter+=1
            if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
                self.restart()
        return self.sensor.co2

