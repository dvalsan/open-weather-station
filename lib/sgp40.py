from pyb import I2C
import time

i2c = I2C(3, I2C.MASTER)

SGP40_ADDRESS = 0x59


def init():
    """Inicializa el sensor, no tiene una fase de inicialización pero según manual está listo después de 0.6ms"""
    """Initialices the sensor, doesn't have an initialization phase, but in the manual specifies that its ready after a 0.6ms waiting time"""
    devices = i2c.scan()
    if SGP40_ADDRESS not in devices:
        raise Exception("Error: SGP40 hasn't been detected")
    time.sleep_ms(1)

def crc8(data):
    """Calculates the CRC-8 with a 0x31 polynomial (x⁸ + x⁵ + x⁴ + 1). It's in the manual."""
    polynomial = 0x31
    crc = 0xFF  # Initial value

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFF

    return crc

def humidityToTicks(rh):
    """Returns all the humidity ticks for the sensor"""
    ticks = int(round((rh * 65535) / 100))
    data = [(ticks >> 8) & 0xFF, ticks & 0xFF]
    return data + [crc8(data)]

def temperatureToTicks(temp):
    """Returns all the temperature ticks for the sensor"""
    ticks = int(round((temp + 45) * 65535 / 175))
    data = [(ticks >> 8) & 0xFF, ticks & 0xFF]
    return data + [crc8(data)]

def getAirQuality(raw_signal):
    """Returns the aire quality depending on the raw value: 
    <10000 Excelent
    >=10000 <30000 Great
    >=30000 <50000 Moderated
    >=50000 Bad
    """
    if raw_signal < 10000:
        return "Excelent"
    elif 10000 <= raw_signal < 30000:
        return "Great"
    elif 30000 <= raw_signal < 50000:
        return "Moderated"
    else:
        return "Bad"

def getAirQualityAbreviated(raw_signal):
    """Returns the aire quality abreviated depending on the raw value:
    <10000 S
    >=10000 <30000 A
    >=30000 <50000 B
    >=50000 F
    """

    if raw_signal < 10000:
        return "S"
    elif 10000 <= raw_signal < 30000:
        return "A"
    elif 30000 <= raw_signal < 50000:
        return "B"
    else:
        return "F"

def readRawValue(humidity = 50, temperature = 25):
    """Returns the raw value of the air quality"""
    tempData = temperatureToTicks(temperature)

    humidityData = humidityToTicks(humidity)

    command = bytearray([0x26, 0x0F]) + bytearray(humidityData) + bytearray(tempData)

    i2c.send(command, SGP40_ADDRESS)
    time.sleep_ms(30) #On themanual says it takes 30ms to get the measurement

    response = i2c.recv(3, SGP40_ADDRESS)

    if crc8(response[:2]) != response[2]:
        raise ValueError("CRC invalid on the response")

    rawValue = (response[0] << 8) | response[1]

    return rawValue
