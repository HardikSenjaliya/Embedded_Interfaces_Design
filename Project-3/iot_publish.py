#!/usr/bin/python3

# Authors -- Isha Sawant and Hardik Senjaliya


import Adafruit_DHT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
 
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("a2ytl2z266nk44-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/certs/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem", "/home/pi/certs/cfd322db94-private.pem.key", "/home/pi/certs/cfd322db94-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if result.is_valid():
        payload = '{ "timestamp": "' + now_str + '","temperature": ' + str(result.temperature) + ',"humidity": '+ str(result.humidity) + ' }'
        print(payload)
        myMQTTClient.publish("thing01/data", payload, 0)
        sleep(4)
    else:
        print (".")
        sleep(1)
