import serial
import signal
import sys
import time
import logging
from sentence import Sentence

class GPS():
    name = 'GPS'
    conn = None
    lastTryTime = None
    numberOfReadTries = 0
    maxNumberOfReadTries = 3
    secondsToWaitForReconnect = 120
    secondsToWaitForRead = 2
    def __init__(self, serialPath, serialBaud, logger=None):
        self.serialPath = serialPath
        self.serialBaud = serialBaud
        self.connect()
    def connect(self):
        self.lastTryTime = int(time.time())
        try:
            self.conn = serial.Serial(self.serialPath,  self.serialBaud)
            self.numberOfReadTries = 0
        except (serial.serialutil.SerialException, OSError) as e:
            print 'Failed to open serial port for GPS'
    def tryReconnect(self):
        currentTime = int(time.time())
        if(currentTime - self.lastTryTime >= self.secondsToWaitForReconnect):
            self.connect()
    def read(self):
	#self.conn.flushOutput()
        if(not self.conn):
            self.tryReconnect()
        while self.conn:
            hasReadTriesLeft = self.numberOfReadTries < self.maxNumberOfReadTries
            if not hasReadTriesLeft:
                break
            line = self.readLine() # '$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47'
            if line[:6] == '$GPGGA':
                sentence = self.getSentence(line)
                if(sentence and sentence.isValid()):
                    #self.logMessage('closing connection') 
                    #self.conn.close()
                    return sentence
            self.numberOfReadTries += 1
            time.sleep(0.1)
        return Sentence([])
    def readLine(self):
        #print 'start of readline'
        try:
            signal.signal(signal.SIGALRM, self.handleReadError)
            signal.alarm(self.secondsToWaitForRead)
            #print 'readLine(): BEFORE READLINE: {}'.format(self.conn.inWaiting())
            line = self.conn.readline()
            self.conn.flushInput()
            #print 'readLine(): AFTER READLINE: {}'.format(self.conn.inWaiting())
            signal.alarm(0)
            self.numberOfReadTries = 0
            return line
        except serial.serialutil.SerialException:
            self.numberOfReadTries += 1
            #print 'Failed to read from serial port'
        return None
    def handleReadError(self, signum, frame):
        pass
    def getSentence(self, line):
        return Sentence(line)
if __name__ == "__main__":
    gps=GPS('/dev/ttyAMA0', 4800)
    coords = gps.read()
    print coords
    print str(coords.latitude) + ', ' + str(coords.longitude)