import grovepi as gpi
import time
from grove_i2c_barometic_sensor_BMP180 import BMP085
from gps import GPS
from lcd import LCD
from modem import SatModem
import csv


TEMP_SENSOR = 0  # Port A0 is for the Temperature Sensor
SOUND_SENSOR = 2  # Port A2 is for the Sound Sensor
bmpSensor = BMP085(0x77, 1)  # Register pressure sensor Port I2C-1
gpsSensor = GPS('/dev/ttyAMA0', 4800)  # Connect Serial to GPS Device
lcdDisplay = LCD()  # Create a reference to the LCD Display
satModem = SatModem('/dev/ttyUSB0')  # Create a Reference to the Sat Modem


secondElapsed = 0

lcdDisplay.setText("Hello!")
time.sleep(2)
lcdDisplay.setText("Prepping Sensors!")
time.sleep(2)
lcdDisplay.setText("Ready to Go!")
time.sleep(2)

with open(str(int(time.time())) + '.csv', 'wb') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(['temperature', 'sound', 'pressure',
                         'latitude', 'longitude', 'altitude'])

while True:
    try:
        lcdDisplay.setText("Gathering Data")
        curTemp = gpi.temp(TEMP_SENSOR)  # Get temperature in celcius
        # Get current sound level in ???
        curSound = gpi.analogRead(SOUND_SENSOR)
        curPressure = bmpSensor.readPressure()/100  # Get current presure in millibar
        curCoords = gpsSensor.read()  # Get the current data from the GPS module

        print str(curTemp) + ', ' + str(curSound) + ', ' + \
            str(curPressure)  # Print Current Readings from Sensors
        print str(curCoords.latitude) + ', ' + str(curCoords.longitude) + \
            ', ' + str(curCoords.altitude)  # Print Current Readings from GPS
        lcdDisplay.setText("Saved Data")

        message = [curCoords.latitude, curCoords.longitude, curCoords.altitude]


        if secondElapsed % 30 == 0:
            # Send Data to Modem
            satModem.sendMessage(str(message))
            lcdDisplay.setText("Sent Data")

        with open('flight.csv', 'a') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow([curTemp, curSound, curPressure,
                                 curCoords.latitude, curCoords.longitude, curCoords.altitude])

    except Exception as e:
        print("Error")
        print(str(e))
        lcdDisplay.setText("Error")

    time.sleep(1)  # Wait 1 Second Until next loop
    secondElapsed += 1
