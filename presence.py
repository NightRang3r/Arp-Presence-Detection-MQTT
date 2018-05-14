import subprocess
from time import sleep
import paho.mqtt.publish as publish


#=========================== SETTINGS ===========================

MQTT_HOST = "127.0.0.1"
MQQT_USER = "mosquitto"
MQTT_PASS = "12345678"
MQTT_TOPIC = "presence"
T_SLEEP = 5


NAMES = ["Bob","Alice"]
MAC_ADDR = ["01:01:01:01:01:01","02:02:02:02:02:02"]

#========================= END SETTINGS =========================

auth = {
   'username':MQQT_USER,
   'password':MQTT_PASS 
}
       
try:
    while True:
        output = subprocess.check_output("sudo arp-scan -l", shell=True)
        for i in range(len(NAMES)):
            if MAC_ADDR[i] in output:
                print(NAMES[i] + " is home")
                publish.single(MQTT_TOPIC + "/" + NAMES[i],"home",hostname=MQTT_HOST, auth=auth)         
            else:
                print(NAMES[i] + " is not_home")
                publish.single(MQTT_TOPIC + "/" + NAMES[i],"not_home",hostname=MQTT_HOST, auth=auth)
            sleep(T_SLEEP)

except:
    print "Something went wrong..."
    pass

