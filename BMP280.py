import time
from py_bmp280.I2CDevice import I2CDevice
from py_bmp280.Exceptions import BMP280Error

class BMP280(I2CDevice):
    data = {
        'CHIP_IDs':                                 [0x56, 0x57, 0x58],
        'I2C_ADDRESS':                              [0x76, 0x77],
        # POWER MODE
        'SLEEP_MODE':                               0x00,
        'FORCED_MODE':                              0x01,
        'NORMAL_MODE':                              0x03,
        'SOFT_RESET':                               0xB6,
        # OVERSAMPLING
        'OVERSAMPLING_SKIP':                        0x00,
        # FILTERING
        'FILTER_COEFF_OFF':                         0x00,
        'FILTER_COEFF_2':                           0x01,
        'FILTER_COEFF_4':                           0x02,
        'FILTER_COEFF_8':                           0x03,
        'FILTER_COEFF_16':                          0x04,
        # STANDBY TIME
        'STANDBY_TIME_1_MS':                        0x00,
        'STANDBY_TIME_63_MS':                       0x01,
        'STANDBY_TIME_125_MS':                      0x02,
        'STANDBY_TIME_250_MS':                      0x03,
        'STANDBY_TIME_500_MS':                      0x04,
        'STANDBY_TIME_1000_MS':                     0x05,
        'STANDBY_TIME_2000_MS':                     0x06,
        'STANDBY_TIME_4000_MS':                     0x07,
        # WORKING MODE
        'ULTRA_LOW_POWER_MODE':                     0x00,
        'LOW_POWER_MODE':                           0x01,
        'STANDART_POWER_MODE':                      0x02,
        'HIGH_RESOLUTION_MODE':                     0x04,
        'ULTRA_HIGH_RESOLUTION_MODE':               0x03,

        'ULTRALOWPOWER_OVERSAMPLING_PRESSURE':      0x01, # X1
        'ULTRALOWPOWER_OVERSAMPLING_TEMPERATURE':   0x01, # X1

        'LOWPOWER_OVERSAMPLING_PRESSURE':           0x02, # X2
        'LOWPOWER_OVERSAMPLING_TEMPERATURE':        0x01, # X1

        'STANDART_OVERSAMPLING_PRESSURE':           0x03, # X4
        'STANDART_OVERSAMPLING_TEMPERATURE':        0x01, # X1

        'HIGH_OVERSAMPLING_PRESSURE':               0x04, # X8
        'HIGH_OVERSAMPLING_TEMPERATURE':            0x01, # X1

        'ULTRAHIGH_OVERSAMPLING_PRESSURE':          0x05, # X16
        'ULTRAHIGH_OVERSAMPLING_TEMPERATURE':       0x02, # X2

        'SEA_LEVEL_PRESSURE':                       1013
    }

    regs = {
        'CHIPID':       0xD0,  # [7:0] Chip ID
        'VERSION':      0xD1,  # [7:0] Microcode version
        'SOFTRESET':    0xE0,  # If 0xB6 written, start reset procedure
        'CAL26':        0xE1,  # Stored in 0xE1:0xF0
        'STATUS':       0xF3,  # 3 - measuring, 0 - really idk what is it
        'CONTROL':      0xF4,  # [7:5] - Temp Oversampling, [4:2] - Pressure Oversampling, [1:0] - power mode
        'CONFIG':       0xF5,  # [7:5] - StandBy Time, [4:2] - Filter, 0 - spi3w_en   
        'PMSB':         0xF7,  # [7:0] => [19:12] pressiure bits
        'PLSB':         0xF8,  # [7:0] => [11:4]  pressiure bits
        'PXLSB':        0xF9,  # [7:4] => [3:0]   pressiure bits
        'TMSB':         0xFA,  # [7:0] => [19:12] temperature bits
        'TLSB':         0xFB,  # [7:0] => [11:4] temperature bits
        'TXLSB':        0xFC,  # [7:4] => [3:0] temperature bits
        'DIG_T1':       0x88,  # 
        'DIG_T2':       0x8A,  #
        'DIG_T3':       0x8C,  #
        'DIG_P1':       0x8E,  #
        'DIG_P2':       0x90,  #
        'DIG_P3':       0x92,  # NVM writted trimming parameters for compensation
        'DIG_P4':       0x94,  #
        'DIG_P5':       0x96,  #
        'DIG_P6':       0x98,  #
        'DIG_P7':       0x9A,  #
        'DIG_P8':       0x9C,  # 
        'DIG_P9':       0x9E   #
    }

    def _getChipID(self): 
        return I2CDevice.read_byte(self, self.regs['CHIPID'])

    def _get_calibration_data(self):
        self.calibration_data['T1'] = I2CDevice.read_byte(self, self.regs['DIG_T1'])
        self.calibration_data['T2'] = I2CDevice.read_byte(self, self.regs['DIG_T2'])
        self.calibration_data['T3'] = I2CDevice.read_byte(self, self.regs['DIG_T3'])
        self.calibration_data['P1'] = I2CDevice.read_byte(self, self.regs['DIG_P1'])
        self.calibration_data['P2'] = I2CDevice.read_byte(self, self.regs['DIG_P2'])
        self.calibration_data['P3'] = I2CDevice.read_byte(self, self.regs['DIG_P3'])
        self.calibration_data['P4'] = I2CDevice.read_byte(self, self.regs['DIG_P4'])
        self.calibration_data['P5'] = I2CDevice.read_byte(self, self.regs['DIG_P5'])
        self.calibration_data['P6'] = I2CDevice.read_byte(self, self.regs['DIG_P6'])
        self.calibration_data['P7'] = I2CDevice.read_byte(self, self.regs['DIG_P7'])
        self.calibration_data['P8'] = I2CDevice.read_byte(self, self.regs['DIG_P8'])
        self.calibration_data['P9'] = I2CDevice.read_byte(self, self.regs['DIG_P9'])

    def _get_raw_data(self):
        self.raw_data['plsb'] = I2CDevice.read_byte(self, self.regs['PLSB'])
        self.raw_data['pmsb'] = I2CDevice.read_byte(self, self.regs['PMSB'])
        self.raw_data['pxsb'] = I2CDevice.read_byte(self, self.regs['PXLSB'])

        self.raw_data['tlsb'] = I2CDevice.read_byte(self, self.regs['TLSB'])
        self.raw_data['tmsb'] = I2CDevice.read_byte(self, self.regs['TMSB'])
        self.raw_data['txsb'] = I2CDevice.read_byte(self, self.regs['TXLSB'])

        temp = 0
        temp = (temp | self.raw_data['tmsb']) << 8;
        temp = (temp | self.raw_data['tlsb']) << 8;
        temp = (temp | self.raw_data['txsb']) >> 4;
        
        self.raw_data['temperature'] = temp

        temp = 0
        temp = (temp | self.raw_data['pmsb']) << 8;
        temp = (temp | self.raw_data['plsb']) << 8;
        temp = (temp | self.raw_data['pxsb']) >> 4;

        self.raw_data['pressure'] = temp

    def __init__(self, bus=-1, addr=-1):
        if addr == -1: 
            try:
                I2CDevice.__init__(self, bus, self.data['I2C_ADDRESS'][0])
            except OSError:
                try: 
                    I2CDevice.__init__(self, bus, self.data['I2C_ADDRESS'][1])
                except:
                    raise BMP280Error("Device Not Found")
        else:
            I2CDevice.__init__(self, bus, addr)

    def update(self):
        self._get_raw_data()
        self.temp = getCelsium(self.raw_data['temperature'])

    def getCelsium(self, t_adc):
        var1 = ((t_adc)/16384.0 - (self.calibration_data['T1'])/1024.0) * (self.calibration_data['T2']);
        var2 = (((t_adc)/131072.0 - (self.calibration_data['T1'])/8192.0) * ((t_adc)/131072.0 - ( self.calibration_data['T1'])/8192.0)) * (self.calibration_data['T3'])
        T = (var1 + var2) / 5120.0
        return T

    def getCelsiumExperimental(self, t_adc):
        v1 = ((((t_adc >> 3) - (self.calibration_data['T1'] << 1))) *
            ( self.calibration_data['T2'])) >> 11
        v2 = (((((t_adc >> 4) - ( self.calibration_data['T1'])) *
            ((t_adc >> 4) - ( self.calibration_data['T1']))) >> 12) *
            ( self.calibration_data['T3'])) >> 14;

        return ((v1 + v2) * 5 + 128) >> 8 

    def reset(self):
        I2CDevice.write_byte(self, self.regs['SOFTRESET'], self.data['SOFT_RESET'])

    def getStatus(self):
        return I2CDevice.read_byte(self, self.regs['STATUS'])

    def getControl(self):
        return I2CDevice.read_byte(self, self.regs['CONTROL'])

    def setControl(self, value):
        I2CDevice.write_byte(self, self.regs['CONTROL'], value)

    def getConfig(self):
        return I2CDevice.read_byte(self, self.regs['CONFIG'])

    def setConfig(self, value):
        I2CDevice.write_byte(self, self.regs['CONFIG'], value)

    def setTemperatureOversampling(self, value):
        curentOversampling = self.getControl() & 0b00011111
        self.setControl(curentOversampling | (value << 5))

    def setPowerMode(self, mode):
        curentMode = self.getControl() & 0b11111100
        self.setControl(curentMode | mode)

    def setStandByTime(self, time):
        config = self.getConfig() & 0b00011111
        self.setConfig(config | (time << 5))

    def setIrrFilter(self, value):
        config = self.getConfig() & 0b11100011
        self.setConfig(config | (value << 2))

    def init(self):
        self.chipID = self._getChipID()
        if not self.chipID in self.data['CHIP_IDs']:
            raise BMP280Error("Unknown ChipID. Your ChipID is {}".format(self.chipID))
        
        self.reset()
        self.setPowerMode(self.data['NORMAL_MODE'])
        self.setTemperatureOversampling(self.data['ULTRAHIGH_OVERSAMPLING_TEMPERATURE'])
        self.setIrrFilter(self.data['FILTER_COEFF_16'])
        self.setStandByTime(self.data['STANDBY_TIME_250_MS'])

        self.calibration_data = dict()
        self._get_calibration_data()
        self.raw_data = dict()
        self._get_raw_data()

        self.update()


    


