from smbus2 import SMBus, i2c_msg
from time import sleep
from math import ceil

compat_ind = 1
i2c_err_str = 'PiicoDev could not communicate with module at address 0x{:02X}, check wiring'
setupi2c_str = ', run "sudo curl -L https://piico.dev/i2csetup | bash". Suppress this warning by setting suppress_warnings=True'


def sleep_ms(t):
    sleep(t/1000)

class I2CBase:
    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        raise NotImplementedError('writeto_mem')

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        raise NotImplementedError('readfrom_mem')

    def write8(self, addr, buf, stop=True):
        raise NotImplementedError('write')

    def read16(self, addr, nbytes, stop=True):
        raise NotImplementedError('read')

    def __init__(self, bus=None, freq=None, sda=None, scl=None):
        raise NotImplementedError('__init__')

class I2CUnifiedLinux(I2CBase):
    def __init__(self, bus=None, suppress_warnings=True):
        if suppress_warnings == False:
            with open('/boot/config.txt') as config_file:
                if 'dtparam=i2c_arm=on' in config_file.read():
                    pass
                else:
                    print('I2C is not enabled. To enable' + setupi2c_str)
                config_file.close()
            with open('/boot/config.txt') as config_file:
                if 'dtparam=i2c_arm_baudrate=400000' in config_file.read():
                    pass
                else:
                    print('Slow baudrate detected. If glitching occurs' + setupi2c_str)
                config_file.close()
        if bus is None:
            bus = 1
        self.i2c = SMBus(bus)

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        data = [None] * nbytes # initialise empty list
        self.smbus_i2c_read(addr, memaddr, data, nbytes, addrsize=addrsize)
        return data
    
    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        self.smbus_i2c_write(addr, memaddr, buf, len(buf), addrsize=addrsize)
    
    def smbus_i2c_write(self, address, reg, data_p, length, addrsize=8):
        ret_val = 0
        data = []
        for index in range(length):
            data.append(data_p[index])
        if addrsize == 8:
            msg_w = i2c_msg.write(address, [reg] + data)
        elif addrsize == 16:
            msg_w = i2c_msg.write(address, [reg >> 8, reg & 0xff] + data)
        else:
            raise Exception('address must be 8 or 16 bits long only')
        self.i2c.i2c_rdwr(msg_w)
        return ret_val
        
    def smbus_i2c_read(self, address, reg, data_p, length, addrsize=8):
        ret_val = 0
        if addrsize == 8:
            msg_w = i2c_msg.write(address, [reg]) # warning this is set up for 16-bit addresses
        elif addrsize == 16:
            msg_w = i2c_msg.write(address, [reg >> 8, reg & 0xff]) # warning this is set up for 16-bit addresses
        else:
            raise Exception('address must be 8 or 16 bits long only')
        msg_r = i2c_msg.read(address, length)
        self.i2c.i2c_rdwr(msg_w, msg_r)
        if ret_val == 0:
            for index in range(length):
                data_p[index] = ord(msg_r.buf[index])
        return ret_val
    
    def write8(self, addr, reg, data):
        if reg is None:
            d = int.from_bytes(data, 'big')
            self.i2c.write_byte(addr, d)
        else:
            r = int.from_bytes(reg, 'big')
            d = int.from_bytes(data, 'big')
            self.i2c.write_byte_data(addr, r, d)
    
    def read16(self, addr, reg):
        regInt = int.from_bytes(reg, 'big')
        return self.i2c.read_word_data(addr, regInt).to_bytes(2, byteorder='little', signed=False)

def create_unified_i2c(bus=None, freq=None, sda=None, scl=None, suppress_warnings=True):    
    return I2CUnifiedLinux(bus=bus, suppress_warnings=suppress_warnings)
