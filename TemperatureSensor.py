"""
Driver for the Si7021 humidity and temperature sensor.
Based on the code found at: https://github.com/herm/Si7021
"""

from time import sleep
import smbus
import ParameterStorage

class Si7021:

    TEMP_MEASURE_HOLD = 0xE3
    TEMP_MEASURE_NO_HOLD = 0xF3

    RH_NO_HOLD = 0xF5
    RH_HOLD = 0xE5
    LAST_TEMPERATURE = 0xE0
    
    READ_HEATER_CTRL = 0x11
    WRITE_HEATER_CTRL = 0x51

    READ_USR_REG = 0xE7
    WRITE_USR_REG = 0xE6

    RESET = 0xFE

    HEATER_OFFSET = 3.09
    HEATER_STEP = 6.074

    USR_RES1 = 128
    USR_VDDS = 64
    USR_HTRE = 4
    USR_RES0 = 1

    lastTemperatureMeasurement =-100
    lastHumidityMeasurement = -100

    TEMPERATURE_PARAM_NAME = "Temperatura"
    RELATIVE_HUMIDITY_PARAM_NAME = "Wilgotność"

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x40
        ParameterStorage.addParameter(self.TEMPERATURE_PARAM_NAME)
        ParameterStorage.addParameter(self.RELATIVE_HUMIDITY_PARAM_NAME)
    
    def persistentBusRead(self, registerAddr, loops=50):
        """ Tries to read from the I2C bus as many times as defined - tries again if exception is raised """
        loopCount =0
        retVal=0
        tryAgain = True        
        while loopCount<=loops and tryAgain:
            try:
                retVal = self.bus.read_word_data(self.addr, registerAddr)
                tryAgain = False
            except:
                loopCount+=1
                sleep(0.5)
        if tryAgain:
            print("Read failed")
        return retVal

    def persistentBusWrite(self, registerAddr, value=None, loops=20):
        """ Tries to write to the I2C bus as many times as defined - tries again if exception is raised """
        loopCount =0        
        tryAgain = True        
        while loopCount<=loops and tryAgain:
            try:                
                if value==None:
                    self.bus.write_bute(self.addr, registerAddr)
                else:
                    self.bus.write_byte(self.addr, registerAddr, value)
                tryAgain = False
            except:
                loopCount+=1
                sleep(0.5)
        if tryAgain:
            print("Write failed")

    def reset(self):
        """ Reset the sensor """
        self.persistentBusWrite(self.RESET)
        #self.bus.write_byte(self.addr, self.RESET)

    def swapBytes(self, word):
        """ Swaps bytes """        
        retVal = ((word & 0xff) << 8) | (word >> 8)
        return retVal

    def readTemp(self, lastTemp=False):  
        """ Reads the temperature from the sensor in degrees Celsius - if lastTemp set to True reads it from the buffer without measurement"""      
        t = self.swapBytes(self.persistentBusRead(self.TEMP_MEASURE_HOLD if not lastTemp else self.LAST_TEMPERATURE))
        t = 175.72 * t / 65536. - 46.85 # recalculated like in DS to degrees Celsius
        ParameterStorage.provideValue(self.TEMPERATURE_PARAM_NAME,t)
        self.lastTemperatureMeasurement=t
        return t

    def readHumidity(self):
        """ Reads the relative humidity from the sensor"""
        rh =self.swapBytes(self.persistentBusRead(self.RH_HOLD))
        rh = 125. * rh  / 65536. - 6 #recalulated like in DS
        rh = max(0, min(100, rh)) #in edge cases results can be over the limit - this is a fix - see DS
        ParameterStorage.provideValue(self.RELATIVE_HUMIDITY_PARAM_NAME,rh)
        self.lastHumidityMeasurement=rh
        return rh

    def read(self):
        """ Read relative humidity and temperature.

        Returns a tuple (rh, temperature)
        """
        rh = self.readHumidity()
        t = self.readTemp(True)
        ParameterStorage.provideValue(self.TEMPERATURE_PARAM_NAME,t)
        ParameterStorage.provideValue(self.RELATIVE_HUMIDITY_PARAM_NAME,rh)
        return (rh, t)

    @property
    def heater_mA(self):
        """ Get heater current in mA """
        usr = self.persistentBusRead(self.READ_USR_REG)#self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        if usr & self.USR_HTRE:
            value = self.persistentBusRead(self.READ_HEATER_CTRL)#self.bus.read_byte_data(self.addr, self.READ_HEATER_CTRL)
            value = value * self.HEATER_STEP + self.HEATER_OFFSET
            return value
        return 0

    @heater_mA.setter
    def heater_mA(self, value):
        """ Set heater current in mA.

        Turing on and off of the heater is handled automatically.
        """
        usr = self.persistentBusRead(self.READ_USR_REG)#self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        if not value:
            usr &= ~self.USR_HTRE
        else:
            # Enable heater and calculate settings
            setting = 0
            if value > self.HEATER_OFFSET:
                value -= self.HEATER_OFFSET
                setting = int(round(value / self.HEATER_STEP)) # See DS 5.5
                setting = min(15, setting) #Avoid overflow
            #self.bus.write_byte_data(self.addr, self.WRITE_HEATER_CTRL, setting)
            usr |= self.USR_HTRE
        self.persistentBusWrite(self.WRITE_USR_REG,usr)#self.bus.write_byte_data(self.addr, self.WRITE_USR_REG, usr)

    def set_resultion(self, bits_rh):
        """ Select measurement resultion.

        bits_rh is the number of bits for the RH measurement. Number of
        bits for temperature is choosen accoring to the table in section 6.1
        of the datasheet.
        """
        usr = self.persistentBusRead(self.READ_USR_REG)#self.bus.read_byte_data(self.addr, self.READ_USR_REG)
        usr &= ~(self.USR_RES0 | self.USR_RES1)
        if bits_rh == 8:
            usr |= self.USR_RES1
        elif bits_rh == 10:
            usr |= self.USR_RES1
        elif bits_rh == 11:
            usr |= self.USR_RES0 | self.USR_RES1
        elif bits_rh != 12:
            raise ValueError("Unsupported number of bits.")
        self.persistentBusWrite(self.WRITE_USR_REG,usr)#self.bus.write_byte_data(self.addr, self.WRITE_USR_REG, usr)


    # Reading the device ID seems to be impossible with the smbus functions
    # as they do not support 2 byte register adresses. And the Si7021 does
    # not accept the address in two transactions
