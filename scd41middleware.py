#import scd4x_rpi
from DFRobot_SCD4X import *
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
    resetWhenCounterIsAbove:int = 15
    lastTemperature:float = 100.0
    lastHumidity:float = 50.0
    lastCO2:int = 0
    reseting:bool = False
    sensor:DFRobot_SCD4X = None
    TEMPERATURE_PARAM_NAME = "Temperatura"
    RELATIVE_HUMIDITY_PARAM_NAME = "Wilgotność"
    CO2_PARAM_NAME = "Stężenie CO2"
    sensorReady:bool = False
    def __init__(self):
        self.sensor = DFRobot_SCD4X()
        while (not self.sensor.begin):
            print("SCD41 sensor not initilised, retrying in 2 seconds...")
            time.sleep(2)  
        print("SCD41 sensor initilised.")
        self.sensor.set_sensor_altitude(80) 
        self.sensor.set_ambient_pressure(100000)
        self.sensor.set_temp_comp(-3.0)
        self.sensor.set_auto_calib_mode(True)         
        self.stop()
        time.sleep(1)
        self.start()
        self.sensorReady = True
        ParameterStorage.addParameter(self.TEMPERATURE_PARAM_NAME,"°C")
        ParameterStorage.addParameter(self.RELATIVE_HUMIDITY_PARAM_NAME,"%")
        ParameterStorage.addParameter(self.CO2_PARAM_NAME,"ppm")

    def start(self):
        print("Starting SCD41 periodic measurement...")
        self.sensor.enable_period_measure(SCD4X_START_PERIODIC_MEASURE)
        time.sleep(5)  # Poczekaj 5 sekund na pierwsze dane pomiarowe

    def stop(self):
        print("Stopping SCD41 periodic measurement...")
        self.sensor.enable_period_measure(SCD4X_STOP_PERIODIC_MEASURE)

    def values(self): 
        print("attempting to read SCD41 values...")   
        if self.sensor.get_data_ready_status and self.sensorReady:
            print("SCD41 data ready, reading measurement...")
            CO2ppm, temp, humidity = self.sensor.read_measurement
            self.readyCounter=0
            self.lastTemperature = temp
            self.lastHumidity = humidity
            self.lastCO2 = CO2ppm
            print(f"SCD41 Readings - CO2: {self.lastCO2} ppm, Temp: {self.lastTemperature:.2f} °C, Humidity: {self.lastHumidity:.2f} %")
        else:
            self.readyCounter+=1
            if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
                self.restart()
        ParameterStorage.provideValue(self.TEMPERATURE_PARAM_NAME,self.lastTemperature)        
        ParameterStorage.provideValue(self.RELATIVE_HUMIDITY_PARAM_NAME,self.lastHumidity)        
        ParameterStorage.provideValue(self.CO2_PARAM_NAME,self.lastCO2)
        return self.lastTemperature, self.lastHumidity, self.lastCO2

    def restart(self):
        print("Restarting SCD41 sensor...")        
        self.reseting = True
        self.sensorReady = False
        try:
            self.stop()
            self.sensor.set_sleep_mode(SCD4X_POWER_DOWN)
            time.sleep(10)
            self.sensor.set_sleep_mode(SCD4X_WAKE_UP)
            time.sleep(1)
            self.sensor.module_reinit
            self.start()
            self.readyCounter = 0
            self.lastTemperature = 100.0
            self.lastHumidity = 50.0
            self.lastCO2 = 0
            print("SCD41 sensor restarted.")
        except Exception as e:
            print(f"Error restarting SCD41 sensor: {e}")
        finally:
            self.reseting = False
            self.sensorReady = True
            
        

    def temperature(self):
        #if self.sensor.get_data_ready_status():
        #    self.sensor.read_measurement()
        #    self.readyCounter=0
        #else:
        #    self.readyCounter+=1
        #    if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
        #        self.restart()
        return self.lastTemperature
    
    def humidity(self):
        #if self.sensor.get_data_ready_status():
        #    self.sensor.read_measurement()
        #    self.readyCounter=0
        #else:
        #    self.readyCounter+=1
        #    if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
        #        self.restart()
        return self.lastHumidity
    
    def co2(self):        
        #if self.sensor.get_data_ready_status():
        #    self.sensor.read_measurement()
        #    self.readyCounter=0
        #else:
        #    self.readyCounter+=1
        #   if self.readyCounter>self.resetWhenCounterIsAbove and not self.reseting:
        #        self.restart()
        return self.lastCO2

