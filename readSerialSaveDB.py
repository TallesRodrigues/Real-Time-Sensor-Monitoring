import serial
import time
import datetime
from datetime import date
import pymongo
from pymongo import MongoClient



#Connection to MongoDB
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.iotDB
collections = db.home

#Open port
mySerialPort = serial.Serial('COM3',9600) #open serial com
time.sleep(10)



#Read Data
data = dict([
	('node_id',0),
	('sensor',''),
	('value',0),
	('_id','')
	])


while True:
	mySerialValue = mySerialPort.readline()  #wait for response on the serial port

	string_decoded = mySerialValue.decode() #decode serial output (byte ->unicode)
	string_decoded = string_decoded.rstrip()     #remove ('\r' & '\n')
	try:
		rc_cmd,node_id,sensor,value = string_decoded.split(',')
		data['node_id'] = int(node_id)
		data['sensor']  = sensor
		data['value'] = int(value)
		#data['_id'] =datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		data['_id'] =datetime.datetime.now()
		print ("Comando "+ rc_cmd)

		if rc_cmd =='Insert':
			print (data) #checking the data you are receiving. Used for development, but can be removed for Production
			post_id = collections.insert_one(data).insert_one

	except:
		time.sleep(10)
		continue
	mySerialPort.flush()
	time.sleep(60) #sleep time in seconds

mySerialPort.close()	   #close the serial com


