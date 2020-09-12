from py_bmp280.I2CDevice import I2CDevice
from py_bmp280.Register import Register


class BMP280(I2CDevice):
    MEAN_SEA_LEVEL_PRESSURE     = 1013
    I2C_ADDRESS1                = 0x76
    I2C_ADDRESS2                = 0x77

    def __init__(self, bus, addr):
        super().__init__(bus, addr)

    def getChipID(self): 
        I2CDevice.read_byte(self, Register.CHIPID)


    


