import grovepi
import time
from grove_i2c_barometic_sensor_BMP180 import BMP085
from gps import GPS
from lcd import LCD

TEMP_SENSOR = 0 # Port A0
SOUND_SENSOR = 2 # Port A2
BMP_SENSOR = BMP085(0x77, 1) # Register pressure sensor Port I2C-1
GPS_SENSOR = GPS('/dev/ttyAMA0', 4800) # Connect Serial to GPS Device
LCD_DISPLAY = LCD()

LCD_DISPLAY.setRGB(0,0, 255)
LCD_DISPLAY.setText("Hello!")
time.sleep(2)
LCD_DISPLAY.setText("Making sure everything is ready!")
time.sleep(3)
LCD_DISPLAY.setText("Ready to Go!")
time.sleep(1)
while True:
    try:
        LCD_DISPLAY.setText("Gathering Sensor Data")
        curTemp = grovepi.temp(TEMP_SENSOR) # Get temperature in celcius
        curSound = grovepi.analogRead(SOUND_SENSOR) # Get current sound level in ???
        curPressure = BMP_SENSOR.readPressure()/100 # Get current presure in millibar
        curAltitude = BMP_SENSOR.readAltitude()  # Get the current altitude in meters
        curCoords = GPS_SENSOR.read() # Get the current data from the GPS module

        print str(curTemp) + ', ' + str(curSound) + ', ' + str(curPressure) + ', ' + str(curAltitude) # Print Current Readings from Sensors
        print str(curCoords.latitude) + ', ' + str(curCoords.longitude) + ', ' + str(curCoords.altitude) # Print Current Readings from GPS
        LCD_DISPLAY.setText("Got Data")

    except:
        print("Error")
        LCD_DISPLAY.setText("Error")

    time.sleep(1) # Wait 1 Second Until next loop