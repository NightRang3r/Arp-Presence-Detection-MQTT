# Arp-Presence-Detection-MQTT

# Description

This script is a based on [https://github.com/initialstate/pi-sensor-free-presence-detector](https://github.com/initialstate/pi-sensor-free-presence-detector)

Scans MAC Addresses using arp-scan and sends message to mqtt broker to determine occupancy.


### Requirements

* Python 2.7
* paho-mqtt
* arp-scan

### Get The Script

<pre>~# cd /home/pi</pre>
<pre>~# wget https://raw.githubusercontent.com/NightRang3r/Arp-Presence-Detection-MQTT/master/presence.py</pre>

You will need to adjust the script with your own parameters in the settings section:

<pre>
MQTT_HOST = "127.0.0.1" - Your MQTT Broker IP Address
MQQT_USER = "mosquitto" - MQTT Broker uSER nAME
MQTT_PASS = "12345678" - MQTT Broker Password
MQTT_TOPIC = "presence" - MQTT Broker Topic
T_SLEEP = 10 - Scan Interval

occupant = ["Bob","Alice"] - Occupants list
address = ["01:01:01:01:01:01","02:02:02:02:02:02"] - MAC Address of each occupant
</pre>


### Install paho-mqtt
<pre>~# sudo pip install paho-mqtt</pre>

### Install arp-scan

<pre>~# sudo apt-get update</pre>
<pre>~# sudo apt-get install arp-scan</pre>

### Create service

<pre>~# cd /etc/systemd/system/</pre>

Create a new file

<pre>~# sudo nano presence.service</pre>

Paste this into the new file and save:

<pre>
[Unit]
Description=Presence
Wants=network.target
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/presence.py
User=root

[Install]
WantedBy=multi-user.target

</pre>

<pre>~# sudo chmod 755 presence.service</pre>

<pre>~# sudo systemctl daemon-reload</pre>
<pre>~# sudo systemctl enable presence.service</pre>
<pre>~# sudo systemctl start presence.service</pre>
<pre>~# sudo systemctl status presence.service</pre>
<pre>~# sudo reboot</pre>


### Home assistant configuration example


**device_tracker.yaml:**

<pre>
- platform: mqtt
  devices:
    bob_arp: presence/bob
    alice_arp: presence/alice
    </pre>

**known_device.yaml** (devices will be generated automatically, just change track value to true):
<pre>
bob_arp:
  hide_if_away: false
  icon:
  mac:
  name: Bob
  picture:
  track: true

alice_arp:
  hide_if_away: false
  icon:
  mac:
  name: Alice
  picture:
  track: true
  </pre>
