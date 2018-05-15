#!/usr/bin/python

import subprocess
from time import sleep
import paho.mqtt.publish as publish
import string, sys
from scapy.all import *


conf.verb = 0

#=========================== SETTINGS ===========================

MQTT_HOST = "127.0.0.1"
MQQT_USER = "mosquitto"
MQTT_PASS = "12345678"
MQTT_TOPIC = "presence"
T_SLEEP = 10
IP_RANGE = "10.0.0.1/24"
DEVICES= {"Bob": "00:00:00:00:00:00", "Alice":"01:01:01:01:01:01"}

#========================= END SETTINGS =========================

auth = {
	'username':MQQT_USER,
	'password':MQTT_PASS 
}

while True:
	try:
		ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IP_RANGE),timeout=2)
		tmpMACS = {}
		for s,r in ans:
			tmpMACS[r.src] = True
		for device in DEVICES:
			if DEVICES[device].lower() in tmpMACS:
				print(device + " is home")
				publish.single(MQTT_TOPIC + "/" + device,"home",hostname=MQTT_HOST, auth=auth)         
			else:
				print(device + " is not_home")
				publish.single(MQTT_TOPIC + "/" + device,"not_home",hostname=MQTT_HOST, auth=auth)
	except Exception, e:
		print e
		print "Something went wrong!"
	sleep(T_SLEEP)
