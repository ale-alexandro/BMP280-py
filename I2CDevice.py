import smbus

class I2CDevice:
    def __init__(self, bus, addr):
        self.bus = smbus.SMBus(bus)
        self.addr = addr

    def read_byte(self, reg):
        return self.bus.read_byte_data(addr, reg)

    def write_byte(self, reg, value):
        return self.bus.write_byte_data(addr, reg, value)
    
    def read_word(self, reg):
        return self.bus.read_word_data(addr, reg)

    def write_word(self, reg, value):
        return self.bus.write_word_data(addr, reg, value)