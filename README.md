# High Altitude Balloon

A simple python setup for a High Altitude Balloon using a Raspberry Pi 2

## Requirements

To use run the following commands on a RPi 2, with GrovePi Hat
```
sudo apt-get update
sudo apt-get install pip
sudo curl -kL dexterindustries.com/update_grovepi | bash
sudo reboot
sudo raspi-config
Interfacing Options -> Serial -> No -> Yes
pip install pynmea2

TEMP:
pip install requests
```

## main.py

main.py contains all the code a student would need to write to have the balloon up and running

## lcd.py

lcd.py contains a simple class for interfacing with the Grove-LCD RGB Backlight

## gps.py

gps.py contains a class for interfacing with the Trimble 63530-00 GPS Modem. It is a modification of the original class from [GoMake](https://github.com/GoMake/gomake-telemetry/blob/master/telemetry/gps.py)

## sentence.py

sentence.py allows for simple reading of the serial data returned in gps.py. This is from [GoMake](https://github.com/GoMake/gomake-telemetry/blob/master/telemetry/sentence.py)