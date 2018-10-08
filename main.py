import grovepi as gpi
import time
from grove_i2c_barometic_sensor_BMP180 import BMP085
from gps import GPS
from lcd import LCD

tempSensor = 0 # Port A0 is for the Temperature Sensor
soundSensor = 2 # Port A2 is for the Sound Sensor
bmpSensor = BMP085(0x77, 1) # Register pressure sensor Port I2C-1
gpsSensor = GPS('/dev/ttyAMA0', 4800) # Connect Serial to GPS Device
lcdDisplay = LCD() # Create a reference to the LCD Display

lcdDisplay.setRGB(0,0, 255) # Set Background Color of Display
lcdDisplay.setText("Hello!")
time.sleep(2)
lcdDisplay.setText("Prepping Sensors!")
time.sleep(2)
lcdDisplay.setText("Ready to Go!")
time.sleep(2)

while True:
    try:
        lcdDisplay.setText("Gathering Sensor Data")
        curTemp = gpi.temp(TEMP_SENSOR) # Get temperature in celcius
        curSound = gpi.analogRead(SOUND_SENSOR) # Get current sound level in ???
        curPressure = bmpSensor.readPressure()/100 # Get current presure in millibar
        curAltitude = bmpSensor.readAltitude()  # Get the current altitude in meters
        curCoords = gpsSensor.read() # Get the current data from the GPS module

        print str(curTemp) + ', ' + str(curSound) + ', ' + str(curPressure) + ', ' + str(curAltitude) # Print Current Readings from Sensors
        print str(curCoords.latitude) + ', ' + str(curCoords.longitude) + ', ' + str(curCoords.altitude) # Print Current Readings from GPS
        lcdDisplay.setText("Got Data")

    except:
        print("Error")
        lcdDisplay.setText("Error")

    time.sleep(1) # Wait 1 Second Until next loop