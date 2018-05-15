import subprocess
from time import sleep
import paho.mqtt.publish as publish


#=========================== SETTINGS ===========================

MQTT_HOST = "127.0.0.1"
MQQT_USER = "mosquitto"
MQTT_PASS = "12345678"
MQTT_TOPIC = "presence"
T_SLEEP = 10
INTERFACE = "eth0"
DEVICES= {"Bob": "00:00:00:00:00:00", "Alice":"01:01:01:01:01:01"}

#========================= END SETTINGS =========================

auth = {
	'username':MQQT_USER,
	'password':MQTT_PASS 
}

while True:
	try:
		output = subprocess.check_output("sudo arp-scan --interface=" + INTERFACE + " --localnet", shell=True)
		for device in DEVICES:
			if DEVICES[device].lower() in output:
				print(device + " is home")
				publish.single(MQTT_TOPIC + "/" + device,"home",hostname=MQTT_HOST, auth=auth)         
			else:
				print(device + " is not_home")
				publish.single(MQTT_TOPIC + "/" + device,"not_home",hostname=MQTT_HOST, auth=auth)
	except:
			print "Something went wrong!"
	sleep(T_SLEEP)
