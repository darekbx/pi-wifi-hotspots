import os
import time
import re

class WifiHotspotsDetect:

	isDebug = False
	isPi = True
	interval = 10
	devices = { "laptop": "wlp4s0", "pi": "wlan0" }
	scanCommand = "sudo iw dev {0} scan"
	fileExtension = ".log"
	fileFormat = "/home/pi/{0}{1}"

	def start(self):
		device = self.devices['pi'] if self.isPi else self.devices['laptop']
		command = self.scanCommand.format(device)
		while True:
			result = command if self.isDebug else os.popen(command).read()
			self.saveResult(result)
			time.sleep(self.interval)

	def saveResult(self, result):
		timestamp = int(time.time())
		fileName = self.fileFormat.format(timestamp, self.fileExtension)
		with open(fileName, 'w') as file:
			file.write(result)
			
	def analyze(self):
		directory = "./data"
		for filename in os.listdir(directory):
			if filename.endswith(self.fileExtension):
				with open(os.path.join(directory, filename), 'rb') as file:
					content = file.readlines()
					self.parseLog(content)
				break

	def parseLog(self, content):
		accessPoints = {}
		currentBss = None
		for line in content:
			line = line.decode('ISO-8859-1')
			result = re.search("^BSS.*$", line)

			if currentBss is not None:
				accessPoints[currentBss].append(line)

			if result is not None:
				currentBss = line[4:21]
				accessPoints[currentBss] = [line]
		
		for bssid in accessPoints: 
			print("BSSID {} has {} properties".format(bssid, len(accessPoints[bssid])))
			
#WifiHotspotsDetect().start()
WifiHotspotsDetect().analyze()