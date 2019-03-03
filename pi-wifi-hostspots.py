import os
import time

class WifiHotspotsDetect:
	
	isDebug = True
	isPi = False
	interval = 10
	devices = { "laptop": "wlp4s0", "pi": "wlan0" }
	scanCommand = "sudo iw dev {0} scan"
	fileExtension = ".log"
	fileFormat = "{0}{1}"

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
		directory = "./"
		for filename in os.listdir(directory):
			if filename.endswith(self.fileExtension):
				with open(filename) as file:
					content = file.readlines()
					print(len(content))

WifiHotspotsDetect().start()
#WifiHotspotsDetect().analyze()