import subprocess
from time import sleep
from threading import Thread
import paho.mqtt.publish as publish


#=========================== SETTINGS ===========================

MQTT_HOST = "127.0.0.1"
MQQT_USER = "mosquitto"
MQTT_PASS = "12345678"
MQTT_TOPIC = "presence"

occupant = ["Alice","Bob"]
address = ["01:01:01:01:01:01","02:02:02:02:02:02"]

#========================= END SETTINGS =========================

auth = {
   'username':MQQT_USER,
   'password':MQTT_PASS 
}




sleep(10)


firstRun = [1] * len(occupant)
presentSent = [0] * len(occupant)
notPresentSent = [0] * len(occupant)
counter = [0] * len(occupant)

def whosHere(i):

    sleep(10)

    while True:

        if stop == True:
            print "Exiting Thread"
            exit()
        else:
            pass

        if address[i] in output:
            print(occupant[i] + " is home")
            publish.single(MQTT_TOPIC + "/" + occupant[i],"home",hostname=MQTT_HOST, auth=auth)
            publish.single(MQTT_TOPIC + "/" + occupant[i],"home",hostname=MQTT_HOST, auth=auth)
            publish.single(MQTT_TOPIC + "/" + occupant[i],"home",hostname=MQTT_HOST, auth=auth)
            if presentSent[i] == 0:
                firstRun[i] = 0
                presentSent[i] = 1
                notPresentSent[i] = 0
                counter[i] = 0
                sleep(10)
            else:
                counter[i] = 0
                sleep(10)
        else:
            print(occupant[i] + " is not_home")
            publish.single(MQTT_TOPIC + "/" + occupant[i],"not_home",hostname=MQTT_HOST, auth=auth)
            publish.single(MQTT_TOPIC + "/" + occupant[i],"not_home",hostname=MQTT_HOST, auth=auth)
            publish.single(MQTT_TOPIC + "/" + occupant[i],"not_home",hostname=MQTT_HOST, auth=auth)
            if counter[i] == 30 or firstRun[i] == 1:
                firstRun[i] = 0
                if notPresentSent[i] == 0:
                    notPresentSent[i] = 1
                    presentSent[i] = 0
                    counter[i] = 0
                else:
                    counter[i] = 0
                    sleep(10)
            else:
                counter[i] = counter[i] + 1
                sleep(10)


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
