# scd4x_rpi.py - Sterownik dla Sensirion SCD4x dla Raspberry Pi (Python 3 / smbus2)
import time
from smbus2 import SMBus # Wymagane na Raspberry Pi (lub smbus)

# Adres I2C czujnika
SCD4X_I2C_ADDR = 0x62

# Komendy SCD4x
CMD_START_PERIODIC_MEASUREMENT = [0x21, 0xAC]
CMD_READ_MEASUREMENT = [0xEC, 0x05]
CMD_GET_DATA_READY_STATUS = [0xE4, 0xB8]
CMD_STOP_PERIODIC_MEASUREMENT = [0x3F, 0x86]

class SCD4X_RPI:
    """Sterownik SCD4x dla Raspberry Pi wykorzystujący smbus2."""
    
    def __init__(self, bus_num=1):
        """
        Inicjalizuje czujnik.
        :param bus_num: Numer magistrali I2C (domyślnie 1 dla RPi).
        """
        self.bus_num = bus_num
        self.addr = SCD4X_I2C_ADDR
        self.co2 = 50
        self.temperature = 100.0
        self.humidity = 50.0
        
        # Otwarcie magistrali I2C
        try:
            self.bus = SMBus(self.bus_num)
            print(f"SCD41: Otwarto magistralę I2C numer {self.bus_num}.")
        except FileNotFoundError:
            print("Błąd: Nie można otworzyć magistrali I2C. Czy jest włączona w raspi-config?")
            raise
        except Exception as e:
            print(f"Błąd inicjalizacji SMBus: {e}")
            raise

    def _crc8(self, data_list):
        """Oblicza 8-bitową sumę kontrolną CRC (polinomial 0x31)."""
        crc = 0xFF
        for byte in data_list:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc = crc << 1
        return crc & 0xFF

    def start_periodic_measurement(self):
        """Rozpoczyna ciągły pomiar. Dane będą gotowe po ~5s."""
        print("SCD41: Rozpoczynanie pomiaru okresowego...")
        # Wysyłanie 2 bajtów komendy
        self.bus.write_i2c_block_data(self.addr, CMD_START_PERIODIC_MEASUREMENT[0], [CMD_START_PERIODIC_MEASUREMENT[1]])
        time.sleep(0.005) # Wymagane opóźnienie po komendzie

    def stop_periodic_measurement(self):
        """Zatrzymuje ciągły pomiar. Wymagane przed innymi komendami."""
        print("SCD41: Zatrzymywanie pomiaru okresowego...")
        # Wysyłanie 2 bajtów komendy
        self.bus.write_i2c_block_data(self.addr, CMD_STOP_PERIODIC_MEASUREMENT[0], [CMD_STOP_PERIODIC_MEASUREMENT[1]])
        time.sleep(0.5) # Wymagane opóźnienie po komendzie (500ms)

    def read_measurement(self):
        """Odczytuje aktualne pomiary (CO2, Temp, Wilgotność)."""
        
        # 1. Wysyła komendę odczytu (komenda z podkomendą)
        # W smbus2 jest to często realizowane przez 'write_i2c_block_data' lub 'write_byte_data'
        self.bus.write_i2c_block_data(self.addr, CMD_READ_MEASUREMENT[0], [CMD_READ_MEASUREMENT[1]])
        time.sleep(0.001)
        
        # 2. Odczytuje 9 bajtów danych (3 x 2 bajty danych + 1 bajt CRC)
        try:
            # Odczyt 9 bajtów z adresu
            data = self.bus.read_i2c_block_data(self.addr, 0x00, 9)
        except Exception as e:
            print(f"Błąd odczytu I2C: {e}")
            return False

        # 3. Walidacja sum kontrolnych (CRC)
        if self._crc8(data[0:2]) != data[2] or \
           self._crc8(data[3:5]) != data[5] or \
           self._crc8(data[6:8]) != data[8]:
            print("SCD41: Błąd sumy kontrolnej (CRC)!")
            return False

        # 4. Parsowanie danych:
        # CO2 (0-1) i CRC (2)
        self.co2 = (data[0] << 8) | data[1]

        # Temperatura (3-4) i CRC (5)
        temp_ticks = (data[3] << 8) | data[4]
        self.temperature = -45 + 175 * (temp_ticks / 65536.0)+3

        # Wilgotność (6-7) i CRC (8)
        hum_ticks = (data[6] << 8) | data[7]
        self.humidity = 100 * (hum_ticks / 65536.0)
        
        return True

    def get_data_ready_status(self):
        """Sprawdza, czy nowe dane pomiarowe są dostępne."""
        
        # Wysyłanie komendy (2 bajty)
        self.bus.write_i2c_block_data(self.addr, CMD_GET_DATA_READY_STATUS[0], [CMD_GET_DATA_READY_STATUS[1]])
        time.sleep(0.001)
        
        # Odczyt 3 bajtów (Status Word + CRC)
        data = self.bus.read_i2c_block_data(self.addr, 0x00, 3)
        
        # Sprawdzenie, czy bit 10 oznacza gotowość (0x07FF - gotowe, 0x0000 - niegotowe)
        status_word = (data[0] << 8) | data[1]
        #print( f"Status word: {status_word:04x}" )
        return (status_word & 0x07FF) != 0