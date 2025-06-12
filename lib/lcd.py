from pyb import I2C
import time

i2c = I2C(3, I2C.MASTER)

LCD_ADDRESS = 0x3E
RGB_ADDRESS = 0x62

LCD_SWAP_TIME = 5

def command(cmd):
    """Send command to the LCD"""
    time.sleep(0.5)
    i2c.send(bytearray([0x80, cmd]), LCD_ADDRESS)

def write(data):
    """Send data (write) to the LCD, the maximum is 16 chars"""
    i2c.send(bytearray([0x40, data]), LCD_ADDRESS)

def init():
    """Initialices the LCD just as the manual says"""
    devices = i2c.scan()
    if LCD_ADDRESS not in devices:
        raise Exception("Error: LCD hasn't been detected")
    if RGB_ADDRESS not in devices:
        raise Exception("Error: RGB controller hasn't been detected")
    command(0x3C)  # Function set
    command(0x0C)  # Display ON, Cursor OFF
    command(0x01)  # Clear display
    time.sleep(0.1)


def clear():
    """Clean the screen"""
    command(0x01)
    time.sleep(0.1)

def setRgb(r, g, b):
    """Sets the screen color following the RGB"""
    i2c.send(bytearray([0x00, 0x00]),RGB_ADDRESS)  # Mode1: Normal mode
    i2c.send(bytearray([0x01, 0x00]), RGB_ADDRESS)  # Mode2: Normal mode
    i2c.send(bytearray([0x08, 0xAA]), RGB_ADDRESS)  # Set PWM frequency
    i2c.send(bytearray([0x04, r]), RGB_ADDRESS)  # Red
    i2c.send(bytearray([0x03, g]), RGB_ADDRESS)  # Green
    i2c.send(bytearray([0x02, b]), RGB_ADDRESS)  # Blue

def writeLine(line, text):
    """Writes a specific text on an specific line (0 is first line, 1 is second)"""
    command(0x80 if line==0 else 0xC0)  # Position the cursor to the start of line 1
    for char in text:
        write(ord(char))

def displayMultiline(text):
    """Simply add a text and it's resposible of separating in two lines if necessary (16 chars each)"""
    clear()
    line0 = text[:16]
    line1 = text[16:]
    writeLine(0, line0)
    writeLine(1, line1)


def displayStats(temp, humidity, accel, airQuality, airQualityRaw):
    """Shows the specific stats, there is more than one line
    First line shows temperature
    Second line shows humidity
    Third line shows airQualityRaw and the Conversion
    Fourth line shows the X value of the Accelerometer
    Fifth line shows the Y and Z value of the Accelerometer
    """
    clear()
    line0 = f"Temp: {temp:.2f}C"
    writeLine(0, line0)

    line1 = f"Humedad:{humidity: .2d}%"
    writeLine(1, line1)

    time.sleep(LCD_SWAP_TIME)
    clear()

    line0 = "Calidad aire:"
    writeLine(0, line0)

    line1 = f"{airQualityRaw} {airQuality}"
    writeLine(1, line1)

    time.sleep(LCD_SWAP_TIME)
    clear()

    line0 = f"Acc(g): X={accel[0]:.2f}"
    writeLine(0, line0)
    line1 = f"Y={accel[1]:.2f} Z={accel[2]:.2f}"
    writeLine(1, line1)

    time.sleep(LCD_SWAP_TIME)
    clear()
