import serial, os
import sys
import requests
import json
import time
import twiggy as tw

tw.quickSetup(file='/home/pi/pachube/pachube.log')
tw.log.info('starting pachube_post.py')

class SimpleSensor:
	def __init__(self, input_string):
		self.get_string_split = input_string[:27].split() # split string but only first 27 characters
		self.temperature = float (int(self.get_string_split[3])*256+int(self.get_string_split[2]))/10
		self.gasMeter = float (int(self.get_string_split[7])*16777216+int(self.get_string_split[6])*65536+int(self.get_string_split[5])*256+int(self.get_string_split[4]))/10
		self.counter = int(self.get_string_split[8])
	def displayValues(self):
	   print "Temperature: ", self.temperature,", GasMeter: ", self.gasMeter,  ", Counter: ", self.counter
	def writeToLogAndCosm(self, id_stream1, id_stream2):
		tw.log.info('logging value gasMeter= ' + str(self.gasMeter))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature}, {"id":id_stream2,"current_value":self.gasMeter}]}
		try:
			resp=requests.put('http://api.pachube.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=5.0)
			if resp.status_code == 200:
				tw.log.info('response value = 200 OK')
			elif resp.status_code == 401:
				tw.log.error('response value = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value = 503 No server error')					
			else:
				tw.log.error('response value unknown = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout')		
		except:
			tw.log.trace('error').warning('Undefined error')

class ComplexSensor:
	def __init__(self, input_string):
		self.get_string_split = input_string[:30].split() # split string but only first 30 characters
		self.temperature = float (int(self.get_string_split[5])*256+int(self.get_string_split[4]))/10
		self.humidity =  (int(self.get_string_split[3])/2)
		self.light = int(self.get_string_split[2])
	def displayValues(self):
	   print "Temperature: ", self.temperature,  "Humidity: ", self.humidity,", Light: ", self.light
	def writeToLogAndCosm(self, id_stream1, id_stream2, id_stream3):
		tw.log.info('logging value ext= ' + str(self.temperature))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature},{"id":id_stream2,"current_value":self.humidity}, {"id":id_stream3,"current_value":self.light}]}
		try:
			resp=requests.put('http://api.pachube.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=5.0)
			if resp.status_code == 200:
				tw.log.info('response value = 200 OK')
			elif resp.status_code == 401:
				tw.log.error('response value = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value = 503 No server error')					
			else:
				tw.log.error('response value unknown = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout')		
		except:
			tw.log.trace('error').warning('Undefined error')

class RoomPressureSensor:
	def __init__(self, input_string):
		self.get_string_split = input_string[:35].split() # split string but only first 35 characters
		self.pressure = float (int(self.get_string_split[7])*256+int(self.get_string_split[6]))/10
		self.temperature = float (int(self.get_string_split[5])*256+int(self.get_string_split[4]))/10
		self.humidity =  (int(self.get_string_split[3])/2)
		self.light = int(self.get_string_split[2])
	def displayValues(self):
	   print "Temperature: ", self.temperature,  "Humidity: ", self.humidity,", Light: ", self.light, "Pressure: ", self.pressure
	def writeToLogAndCosm(self, id_stream1, id_stream2, id_stream3, id_stream4):
		tw.log.info('logging value ext= ' + str(self.temperature))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature},{"id":id_stream2,"current_value":self.humidity}, {"id":id_stream3,"current_value":self.light}, {"id":id_stream4,"current_value":self.pressure}]}
		try:
			resp=requests.put('http://api.pachube.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=5.0)
			if resp.status_code == 200:
				tw.log.info('response value = 200 OK')
			elif resp.status_code == 401:
				tw.log.error('response value = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value = 503 No server error')					
			else:
				tw.log.error('response value unknown = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout')		
		except:
			tw.log.trace('error').warning('Undefined error')			
			
class ElectroPower:
	def __init__(self, input_string):
		self.get_string_split = input_string[:30].split() # split string but only first 30 characters
		self.power1 = int(self.get_string_split[3])*256+int(self.get_string_split[2])
		self.power2 = int(self.get_string_split[5])*256+int(self.get_string_split[4])
		self.power3 = int(self.get_string_split[7])*256+int(self.get_string_split[6])
		self.power123 = self.power1 + self.power2 + self.power3
		#usekwh += float((self.power1 + self.power2 + self.power3) * 0.2) / 3600000;
	def displayValues(self):
	   print "Power1: ", self.power1,  "Power2: ", self.power2,", Power3: ", self.power3
	   print "Power123: ", self.power123   
	def writeToLogAndCosm(self, id_stream1):
		tw.log.info('logging value Epower= ' + str(self.power123))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.power123},]}
		try:
			resp=requests.put('http://api.pachube.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=5.0)
			if resp.status_code == 200:
				tw.log.info('response value = 200 OK')
			elif resp.status_code == 401:
				tw.log.error('response value = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value = 503 No server error')					
			else:
				tw.log.error('response value unknown = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout')		
		except:
			tw.log.trace('error').warning('Undefined error')			
			
PORT = '/dev/ttyUSB0'	# set tty port
BAUD_RATE = 57600
serial_port = serial.Serial(PORT, BAUD_RATE)	#open serial port

# authentication headers
headers = {"X-PachubeApiKey": "vi2cY7xBsOtFX-5dswzekyaFcYzbLUaaHWxQRXwrgN0"}

# send meassured value to pachube in json format when new message from sensor arrives
while True:
	serial_string = serial_port.readline()	#read line from tty

	#thermocouple sensor and gas meter id=22
	if serial_string[:5] == "OK 22": 										    
		int_sens = SimpleSensor(serial_string)
		int_sens.displayValues()
		int_sens.writeToLogAndCosm("T22", "Gas")
	
	#external sensor roomNode id=1
	if (serial_string[:5] == "OK 1 ") or (serial_string[:5] == "OK 33"):	
		ext_sens = ComplexSensor(serial_string)
		ext_sens.displayValues()
		ext_sens.writeToLogAndCosm("Tout", "Xout", "Lout")

	#internal sensor roomNode id=5
	if serial_string[:5] == "OK 5 ":										
		int5_sens = RoomPressureSensor(serial_string)
		int5_sens.displayValues()
		int5_sens.writeToLogAndCosm("Tin5", "Xin5", "Lin5", "P5")			

	#internal sensor roomNode id=9
	if serial_string[:5] == "OK 9 ":										
		int9_sens = ComplexSensor(serial_string)
		int9_sens.displayValues()
		int9_sens.writeToLogAndCosm("Tin9", "Xin9", "Lin9")	
		
	#Power of Electicity id=2
	if serial_string[:5] == "OK 2 ":										
		elPow = ElectroPower(serial_string)
		elPow.displayValues()
		elPow.writeToLogAndCosm("Epower")	
	
	#Send time
	#serial_port.write("hello")