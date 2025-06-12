from pyb import I2C
import time

i2c = I2C(3, I2C.MASTER)

LIS3DHTR_I2C_ADDR = 0x19

# Main registers
WHO_AM_I = 0x0F
CTRL_REG1 = 0x20
CTRL_REG4 = 0x23
STATUS_REG = 0x27
OUT_X_L = 0x28
OUT_Y_L = 0x2A
OUT_Z_L = 0x2C


def init():
    """Initialice the accelerometer, 
    we use the base values of 100Hz reading and with the sensors X, Y, Z 
    activated with a configured range of ±2g"""
    devices = i2c.scan()
    if LIS3DHTR_I2C_ADDR not in devices:
        raise Exception("Error: LIS3DH hasn't been detected")

    # Activate, 100Hz, XYZ active
    i2c.mem_write(bytearray([0x57]), LIS3DHTR_I2C_ADDR, CTRL_REG1)

    # ±2g, data in 16 bits
    i2c.mem_write(bytearray([0x00]), LIS3DHTR_I2C_ADDR, CTRL_REG4)


def readRegister(reg, nbytes=1):
    """Reads the indicated register, it's done like this to make the code easier to read"""
    return i2c.mem_read(nbytes, LIS3DHTR_I2C_ADDR, reg)

def writeRegister(reg, data):
    """Writes the indicated register, it's done like this to make the code easier to read"""
    i2c.mem_write(bytearray([data]), LIS3DHTR_I2C_ADDR, reg)

def isDataReady():
    """Verifies if there is new data availlable (bit 3 on STATUS_REG)"""
    status = readRegister(STATUS_REG, 1)[0]
    return (status & 0x08) != 0

def readAcceleration():
    """Reads the acceleration on X, Y, Z and returns it in g"""
    if not isDataReady():
        return None  # No new data

    # Read 6 byes (X, Y, Z - 16 bits each)
    data = readRegister(OUT_X_L, 6)

    def convert(raw_l, raw_h):
        """Aux method to convert from raw to value"""
        value = (raw_h << 8) | raw_l
        if value & 0x8000:  
            value -= 65536
        return value / 16384  # Scale to g (for ±2g)

    ax = convert(data[0], data[1])
    ay = convert(data[2], data[3])
    az = convert(data[4], data[5])

    return (ax, ay, az)

def setRange(scale):
    """Configures the measure range on ±2g, ±4g, ±8g, ±16g"""
    ranges = {2: 0x00, 4: 0x10, 8: 0x20, 16: 0x30}
    if scale not in ranges:
        raise ValueError("Not a valid range, use: 2, 4, 8 or 16g")

    current = readRegister(CTRL_REG4, 1)[0]
    newValue = (current & 0xCF) | ranges[scale]
    writeRegister(CTRL_REG4, newValue)
