import subprocess
from time import sleep
from threading import Thread
import paho.mqtt.publish as publish

#=========================== SETTINGS ===========================

MQTT_HOST = "127.0.0.1"
MQQT_USER = "mosquitto"
MQTT_PASS = "12345678"
MQTT_TOPIC = "presence"
T_SLEEP = 10

occupant = ["Bob","Alice"]
address = ["01:01:01:01:01:01","02:02:02:02:02:02"]

#========================= END SETTINGS =========================

auth = {
   'username':MQQT_USER,
   'password':MQTT_PASS 
}


def whosHere(i):
    while True:
        sleep(T_SLEEP)
        if stop == True:
            print "Exiting Thread"
            exit()
        else:
            pass

        if address[i] in output:
            print(occupant[i] + " is home")
            publish.single(MQTT_TOPIC + "/" + occupant[i],"home",hostname=MQTT_HOST, auth=auth)         
        else:
            print(occupant[i] + " is not_home")
            publish.single(MQTT_TOPIC + "/" + occupant[i],"not_home",hostname=MQTT_HOST, auth=auth)
try:

    global stop
    stop = False
    for i in range(len(occupant)):
        t = Thread(target=whosHere, args=(i,))
        t.start()

    while True:
        global output
        output = subprocess.check_output("sudo arp-scan -l", shell=True)
        sleep(10)

except KeyboardInterrupt:
    stop = True
    exit()