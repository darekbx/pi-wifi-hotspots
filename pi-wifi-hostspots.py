import os
import time

class WifiHotspotsDetect:
	
	isDebug = True
	isPi = False
	interval = 10
	devices = { "laptop": "wlp4s0", "pi": "wlan0" }
	scanCommand = "sudo iw dev {0} scan"
	fileFormat = "{0}.log"

	def start(self):
		device = self.devices['pi'] if self.isPi else self.devices['laptop']
		command = self.scanCommand.format(device)
		while True:
			result = None
			if self.isDebug:
				result = command
			else:  
				result = os.popen(command).read()
			self.saveResult(result)
			time.sleep(self.interval)

	def saveResult(self, result):
		timestamp = int(time.time())
		fileName = self.fileFormat.format(timestamp)
		with open(fileName, 'w') as file:
			file.write(result)

WifiHotspotsDetect().start()
