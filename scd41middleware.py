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

    sensor:scd4x_rpi.SCD4X_RPI = None
    TEMPERATURE_PARAM_NAME = "Temperatura"
    RELATIVE_HUMIDITY_PARAM_NAME = "Wilgotność"
    CO2_PARAM_NAME = "Stężenie CO2"

    def __init__(self):
        self.sensor = scd4x_rpi.SCD4X_RPI()
        self.stop()
        self.start()
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
        ParameterStorage.provideValue(self.TEMPERATURE_PARAM_NAME,self.sensor.temperature)        
        ParameterStorage.provideValue(self.RELATIVE_HUMIDITY_PARAM_NAME,self.sensor.humidity)        
        ParameterStorage.provideValue(self.CO2_PARAM_NAME,self.sensor.co2)
        return self.sensor.temperature, self.sensor.humidity, self.sensor.co2

    def temperature(self):
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
        return self.sensor.temperature
    
    def humidity(self):
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
        return self.sensor.humidity
    
    def co2(self):
        if self.sensor.get_data_ready_status():
            self.sensor.read_measurement()
        return self.sensor.co2

