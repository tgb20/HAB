import sys
import time
import rockBlock
from rockBlock import rockBlockProtocol
from lcd import LCD

lcdDisplay = LCD()


def print_out_waiting(conn, msg):
	buffer_size = str(conn.outWaiting())
	logging.info(msg + buffer_size)


class SatModem (rockBlockProtocol):
	devPath = "/dev/tty.usbserial-FT0DJGSK"

	def __init__(self, satPath, logger=None):
		self.devPath = satPath
		self.modem = None
		self.connect()

	def connect(self):
		print("Attempting to connect to satellite")
		try:
			print self.devPath
			self.modem = rockBlock.rockBlock(self.devPath, self)
			print(self.modem.s, 'connect():AFTER DEFAULT CONNECT:')
			dir(self.modem)
		except Exception as e:
			print('Satellite failed to initialize')
			print("Error" + str(e))
			lcdDisplay.setText('INIT FAILED')
	def sendMessage(self, message):
		if(self.modem):
			print(self.modem.s,'sendMessage():BEFORE SENDMESSAGE:')
			self.modem.sendMessage(message)
		else:
			self.connect()
			print(self.modem.s,'sendMessage()->connect():AFTER CONNECT:')
	def rockBlockTxStarted(self):
		print("Establishing satellite connection...") 
		lcdDisplay.setText('TX CONNECTING')  
	def rockBlockTxFailed(self):
		print(self.modem.s,'rockBlockTxFailed():BEFORE FLUSH:')
		print("Satellite transmission failed...")
		lcdDisplay.setText('TX FAILED')  
		self.modem.s.flushOutput()
		print(self.modem.s,'rockBlockTxFailed():AFTER FLUSH:')
	def rockBlockTxSuccess(self,messageNumber):
		print("Satellite transmission succeeded for message " + str(messageNumber))
		print(self.modem.s, 'rockBlockTxSuccess():AFTER TX SUCCEED EVENT:')
		lcdDisplay.setText('TX SUCCEEDED') 
		
if __name__ == '__main__':
	messageString = "Sat Modem Test"
	s = SatModem('/dev/ttyUSB0')
	# g = gps.GPS('/dev/ttyAMA0', 4800, s.logger)
	# coordinates = g.read()
	# print str(coordinates.latitude) + ', ' + str(coordinates.longitude)
	# timestamp =time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	# record = flightrecord.FlightRecord(timestamp, coordinates, {"Sound": "368", "Gas": "0.4717", "Barometer": "1010.39", "Temperature": "30.20"})
	# s.sendMessage(record.getSatModemFormat())
	# s.sendMessage(messageString)
