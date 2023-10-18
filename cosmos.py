import RPi.GPIO as GPIO
import time
import urllib2
import json
import time
import Adafruit_DHT
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import preprocessing
import pandas as pd
import blynklib
pin=27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.IN) #gas
GPIO.setup(27,GPIO.IN) #temperature 
GPIO.setup(17,GPIO.IN) #soil
sensor = Adafruit_DHT.DHT11
df=pd.read_csv("Weather3.csv")
X = df[['HUMIDITY', 'TEMPERATURE']]
y = df['WEATHER FORECAST']
reg = linear_model.LinearRegression()
reg.fit(df[['HUMIDITY', 'TEMPERATURE']], df['WEATHER FORECAST'])
BLYNK_AUTH='MFm4vv9TsmdTdpYrMvWLOFShmVkyfN1I'
blynk=blynklib.Blynk(BLYNK_AUTH)
'''def sendNotification(token, channel, message):
	data = {
		"body" : message,
		"message_type" : "text/plain"
	}
	req = urllib2.Request('http://api.pushetta.com/api/pushes/{0}/'.format(channel))
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'Token {0}'.format(token))
	response = urllib2.urlopen(req, json.dumps(data))'''
i=0
while(True):
	print("REPORT NO: ",i)
	i=i+1
	x=GPIO.input(2)
	y=GPIO.input(17)
	if x==0 and y==0 :
		print("gas detected")
		print("Water Detected")
		try:
                        blynk.run()
			print("Reading PIR status")
			blynk.notify('EMERGENCY !!! \n Your farm is on Fire')
			print("Fire Detected")
		except KeyboardInterrupt:
			print("Exit")
			GPIO.cleanup()
	elif x==0 and y==1:
		print("gas present")
		try:
			print("Reading PIR status")
			blynk.notify('Your farm is on Fire /n Water Level is also Decreased ')
			print("fire")
		except KeyboardInterrupt:
			print("Exit")
			GPIO.cleanup()
	elif x==1 and y==0:
		print("All is well! xD")
	elif x==1 and y==1:
		try:
			print("11111111Reading PIR status")
		        blynk.notify('Alert!! no water for farming\n switch on the irrigation system')
			print("no water")
		except KeyboardInterrupt:
			print("Exit")#
			GPIO.cleanup()
		time.sleep(10)

		#machinelearning:
	else:
		print("sensor not working")
	while (True):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
			fahrenheit=float((temperature*1.8)+32)  #formula
			X = df[['HUMIDITY', 'TEMPERATURE']]
			y = df['WEATHER FORECAST']
			le = preprocessing.LabelEncoder()#making LabelEncoder function varibale
			df = df.apply(le.fit_transform)#used to convert string values into integer values
			reg = linear_model.LinearRegression()
			reg.fit(df[['HUMIDITY', 'TEMPERATURE']], df['WEATHER FORECAST'])
			print("WEATHER REPORT")
			print(reg.predict([[humidity,fahrenheit]]))


			if(float(reg.predict([[humidity,fahrenheit]]))>=0 and float(reg.predict([[humidity,fahrenheit]]))<1):
				try:
                                        blynk.notify('Light rain')
					print("light rain")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif(float(reg.predict([[humidity,fahrenheit]]))>=1 and float(reg.predict([[humidity,fahrenheit]]))<2):
				try:
					blynk.notify('Broken Clouds')
					print("Broken Clouds")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]]))>=2 and float(reg.predict([[humidity, fahrenheit]])) < 3):
				try:
					blynk.notify('Proximity Shower Rain')
					print("Proximity Shower Rain ")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]]))>=3 and float(reg.predict([[humidity, fahrenheit]])) < 4):
				try:
					blynk.notify('Sky is Clear')
					print("Sky is Clear")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]]))>=4 and float(reg.predict([[humidity, fahrenheit]])) < 5):
				try:
					blynk.notify('Scattered Clouds"')
					print("Scattered Clouds")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 5 and float(reg.predict([[humidity, fahrenheit]])) < 6):
				try:
					blynk.notify('Few Clouds')
					print("Few Clouds")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 6 and float(reg.predict([[humidity, fahrenheit]])) < 7):
				try:
					blynk.notify('Squalls')
					print("Squalls")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 7 and float(reg.predict([[humidity, fahrenheit]])) < 8):
				try:
					blynk.notify('Overcast Clouds')
					print("Overcast clouds ")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 8 and float(reg.predict([[humidity, fahrenheit]])) < 9):
				try:
					blynk.notify('Heavy Snow')
					print("Heavy Snow")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 9 and float(reg.predict([[humidity, fahrenheit]])) < 10):
				try:
					blynk.notify('Mist')
					print("Mist")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 10 and float(reg.predict([[humidity, fahrenheit]])) < 11):
				try:
					blynk.notify('Haze')
					print("Haze")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			elif (float(reg.predict([[humidity, fahrenheit]])) >= 11 and float(reg.predict([[humidity, fahrenheit]])) < 12):
				try:
					blynk.notify('Fog')
					print("Fog")
				except KeyboardInterrupt:
					print("Exit")
					GPIO.cleanup()
			else:
				print("not predicted")
		else:
			print('Failed to get reading. Try again!')

		time.sleep(10)
		break