from pyb import I2C
import time

i2c = I2C(3, I2C.MASTER)

AHT20_ADDRESS = 0x38
ATH_MAX_TIMEOUT = 20

def init():
    """Start and calibrates the sensor"""
    devices = i2c.scan()
    if AHT20_ADDRESS not in devices:
        raise Exception("Error: AHT20 hasn't been detected")
    i2c.send(bytearray([0xBE, 0x08, 0x00]), AHT20_ADDRESS)
    time.sleep_ms(10)   # 10ms waiting time due to manual reccomendation


def is_busy():
    """Returns true if the sensor is busy"""
    status = i2c.recv(1, AHT20_ADDRESS)[0]  # Read status
    return (status & 0b10000000) != 0  # Extract bit 7 (BUSY)


def read():
    """Send measure order and return a pair (temperature, humidity)"""
    i2c.send(bytearray([0xAC, 0x33, 0x00]), AHT20_ADDRESS)

    time.sleep_ms(80) # 80ms waiting time due to manual reccomendation

    # Make it wait just in case it didn't finished
    acum_time = 0
    while(is_busy()):
        time.sleep(0.1)
        acum_time = acum_time + 0.1
        if acum_time >= ATH_MAX_TIMEOUT:
            print("Error measuring temperature and humidity")
            return -1,-1;

    # Read the 6 data bytes
    data = i2c.recv(6, AHT20_ADDRESS)

    # Verify there is valid data
    if len(data) < 6:
        return None, None

    # Convert the humidity and temperature data
    raw_humidity = (data[1] << 16) | (data[2] << 8) | data[3]
    raw_humidity = raw_humidity >> 4  # Remove the 4 status bites
    humidity = (raw_humidity * 100) / (1 << 20)  # Scale the percentage

    raw_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
    temperature = (raw_temp * 200 / (1 << 20)) - 50  # Convert to °C

    return temperature, humidity
