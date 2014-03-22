# Gateway between Xively and JeeNodes sensors
# Programmed by Igor Steiner
# 2014-03-15	correct the log and diagnostic code
# 2014-03-22	bug fixes

import serial, os
import sys
import requests
import json
import time
import twiggy as tw

tw.quickSetup(file='/home/pi/pachube/pachube.log')
tw.log.info('starting pachube_post.py')
firstStart=True
previousGasMeterHour = previousGasMeterDay = previousGasMeterMonth = 0
diffGasMeterHour = diffGasMeterDay = diffGasMeterMonth = 0
t0_hour = t0_day = t0_month = time.localtime()
print "time: ",time.asctime()

class SimpleSensor:
	def __init__(self, input_string):
		self.get_string_split = input_string[:27].split() # split string but only first 27 characters
		self.temperature = float (int(self.get_string_split[3])*256+int(self.get_string_split[2]))/10
		self.gasMeter = float (int(self.get_string_split[7])*16777216+int(self.get_string_split[6])*65536+int(self.get_string_split[5])*256+int(self.get_string_split[4]))/10
		self.counter = int(self.get_string_split[8])
	def displayValues(self):
	   print "Temperature: ", self.temperature,", GasMeter: ", self.gasMeter,  ", Counter: ", self.counter
	def writeToLogAndCosm(self, id_stream1, id_stream2):
		# calculate gas meter increment on time periods: hour, day, month
		global firstStart
		global t0_hour
		global t0_day
		global t0_month
		global previousGasMeterHour
		global previousGasMeterDay
		global previousGasMeterMonth
		global diffGasMeterHour
		global diffGasMeterDay
		global diffGasMeterMonth
		if firstStart == True:
			firstStart = False
			t0_hour = t0_day = t0_month = time.localtime()
			previousGasMeterHour = previousGasMeterDay = previousGasMeterMonth = self.gasMeter
		else:
			self.t = time.localtime()
			#print 'Hour:', self.t.tm_hour, ' Day:', self.t.tm_mday, ' Month:', self.t.tm_mon
			if self.t.tm_hour <> t0_hour.tm_hour:
				diffGasMeterHour = round(self.gasMeter - previousGasMeterHour,2)
				#print " diffGasMeterHour: ", diffGasMeterHour
				previousGasMeterHour = self.gasMeter
				t0_hour = self.t
			if self.t.tm_mday <> t0_day.tm_mday:
				diffGasMeterDay = round(self.gasMeter - previousGasMeterDay, 2)
				#print " diffGasMeterDay: ", diffGasMeterDay
				previousGasMeterDay = self.gasMeter
				t0_day = self.t
			if self.t.tm_mon <> t0_month.tm_mon:
				diffGasMeterMonth = round(self.gasMeter - previousGasMeterMonth,2)
				#print " diffGasMeterMonth: ", diffGasMeterMonth
				previousGasMeterMonth = self.gasMeter
				t0_month = self.t				
		#tw.log.info('logging value gasMeter= ' + str(self.gasMeter))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature}, {"id":id_stream2,"current_value":self.gasMeter}, {"id":"GasHour","current_value":diffGasMeterHour}, {"id":"GasDay","current_value":diffGasMeterDay}, {"id":"GasMonth","current_value":diffGasMeterMonth}]}
		try:
			resp=requests.put('https://api.xively.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=500.0)
			if resp.status_code == 200:
				#print " Response gasMeter - 200 -ok"
				#tw.log.info('response value gasMeter = 200 OK')
				pass  
			elif resp.status_code == 401:
				tw.log.error('response value gasMeter = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value gasMeter = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value gasMeter = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value gasMeter = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value gasMeter = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value gasMeter = 503 No server error')					
			else:
				tw.log.error('response value unknown gasMeter = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout gasMeter')		
		except:
			tw.log.trace('error').warning('Undefined error gasMeter')

class ComplexSensor:
	def __init__(self, input_string):
		self.get_string_split = input_string[:30].split() # split string but only first 30 characters
		self.temperature = float (int(self.get_string_split[5])*256+int(self.get_string_split[4]))/10
		#check negative number
		if self.temperature > 51.2:
			self.temperature = round(self.temperature - 102.4,1)
		self.humidity =  (int(self.get_string_split[3])/2)
		self.light = int(self.get_string_split[2])
	def displayValues(self):
	   print "Temperature: ", self.temperature,  "Humidity: ", self.humidity,", Light: ", self.light
	def writeToLogAndCosm(self, id_stream1, id_stream2, id_stream3):
		#tw.log.info('logging value ext= ' + str(self.temperature))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature},{"id":id_stream2,"current_value":self.humidity}, {"id":id_stream3,"current_value":self.light}]}
		try:
			resp=requests.put('https://api.xively.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=500.0)
			if resp.status_code == 200:
				#print " Response RoomNode - 200 -ok"
				#tw.log.info('response value RoomNode = 200 OK')
				pass  
			elif resp.status_code == 401:
				tw.log.error('response value RoomNode = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value RoomNode = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value RoomNode = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value RoomNode = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value RoomNode = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value RoomNode = 503 No server error')					
			else:
				tw.log.error('response value unknown RoomNode = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout RoomNode')		
		except:
			tw.log.trace('error').warning('Undefined error RoomNode')

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
		#tw.log.info('logging value ext= ' + str(self.temperature))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.temperature},{"id":id_stream2,"current_value":self.humidity}, {"id":id_stream3,"current_value":self.light}, {"id":id_stream4,"current_value":self.pressure}]}
		try:
			resp=requests.put('https://api.xively.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=500.0)
			if resp.status_code == 200:
				#print " Response RoomPressure - 200 -ok"
				#tw.log.info('response value RoomPressure = 200 OK')
				pass  
			elif resp.status_code == 401:
				tw.log.error('response value RoomPressure = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value RoomPressure = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value RoomPressure = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value RoomPressure = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value RoomPressure = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value RoomPressure = 503 No server error')					
			else:
				tw.log.error('response value unknown RoomPressure = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout RoomPressure')		
		except:
			tw.log.trace('error').warning('Undefined error RoomPressure')			
			
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
		#tw.log.info('logging value Epower= ' + str(self.power123))	
		data={"version":"1.0.0","datastreams":[{"id":id_stream1,"current_value":self.power123},]}
		params = {'field3': self.power123,'key':'NJQGS40ZVNGNK36S'}
		try:
			resp=requests.put('https://api.xively.com/v2/feeds/40500',headers=headers,data=json.dumps(data),timeout=500.0)							
			#respThingSpeak=requests.post('http://api.thingspeak.com/update',headers=headerThingSpeak, data=params,timeout=50.0)
			if resp.status_code == 200:
				#print " Response Epower - 200 -ok"
				#tw.log.info('response value Epower = 200 OK')
				pass  
			elif resp.status_code == 401:
				tw.log.error('response value Epower = 401 Not Authorized')
			elif resp.status_code == 403:
				tw.log.error('response value Epower = 403 Forbidden')				
			elif resp.status_code == 404:
				tw.log.error('response value Epower = 404 Not Found')				
			elif resp.status_code == 422:
				tw.log.error('response value Epower = 422 Unprocessable Entity')			
			elif resp.status_code == 500:
				tw.log.error('response value Epower = 500 Internal Server Error')		
			elif resp.status_code == 503:
				tw.log.error('response value Epower = 503 No server error')					
			else:
				tw.log.error('response value unknown Epower = ' + str(resp.status_code))
		except requests.exceptions.Timeout:
			tw.log.trace('error').warning('Timeout Epower')		
		except:
			tw.log.trace('error').warning('Undefined error Epower')			
			
PORT = '/dev/ttyUSB0'	# set tty port
BAUD_RATE = 57600
serial_port = serial.Serial(PORT, BAUD_RATE)	#open serial port

# authentication headers
headers = {"X-PachubeApiKey": "vi2cY7xBsOtFX-5dswzekyaFcYzbLUaaHWxQRXwrgN0"}
#headerThingSpeak = {'key=NJQGS40ZVNGNK36S&field1=222'}
headerThingSpeak = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

# send measured value to pachube in json format when new message from sensor arrives
while True:
	serial_string = serial_port.readline()	#read line from tty

	#thermocouple sensor and gas meter id=22
	if serial_string[:5] == "OK 22": 										    
		int_sens = SimpleSensor(serial_string)
		#int_sens.displayValues()
		int_sens.writeToLogAndCosm("T22", "Gas")
	
	#external sensor roomNode id=1
	if (serial_string[:5] == "OK 1 ") or (serial_string[:5] == "OK 33"):	
		ext_sens = ComplexSensor(serial_string)
		#ext_sens.displayValues()
		ext_sens.writeToLogAndCosm("Tout", "Xout", "Lout")

	#internal sensor roomNode id=5
	if serial_string[:5] == "OK 5 ":										
		int5_sens = RoomPressureSensor(serial_string)
		#int5_sens.displayValues()
		int5_sens.writeToLogAndCosm("Tin5", "Xin5", "Lin5", "P5")			

	#internal sensor roomNode id=9
	if serial_string[:5] == "OK 9 ":										
		int9_sens = ComplexSensor(serial_string)
		#int9_sens.displayValues()
		int9_sens.writeToLogAndCosm("Tin9", "Xin9", "Lin9")	
		
	#Power of Electicity id=2
	if serial_string[:5] == "OK 2 ":										
		elPow = ElectroPower(serial_string)
		#elPow.displayValues()
		elPow.writeToLogAndCosm("Epower")	
	
	#Send time
	#serial_port.write("hello")
