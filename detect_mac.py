#!/usr/bin/python

'''
Requirements:

 python 2.7
 pip install scapy
 pip install json
 
'''

import string, sys, time
from scapy.all import *
conf.verb = 0
import json
import os.path

IP_RANGE = "10.0.0.1/24"
T_SLEEP = 10

def loadOrCreateMacs():
	tmpMacs = {}
	if not os.path.isfile("macs.json"):
		file = open("macs.json","w")
		file.write(json.dumps(tmpMacs))
		file.close()
	else:
		file = open("macs.json","r")
		tmpMacs = json.loads(file.read())
		file.close()
	return tmpMacs

def saveMacFile(pMacs):
	file = open("macs.json", "w")
	file.write(json.dumps(pMacs))
	file.close()

def macExists(macAddr):
	macs = loadOrCreateMacs()
	return macAddr in macs
	
def removeMac(macAddr):
	macs = loadOrCreateMacs()
	if (macAddr in macs):
		del macs[macAddr]
		saveMacFile(macs)

def addMac(macAddr):
	macs = loadOrCreateMacs()
	macs[macAddr] = True
	saveMacFile(macs)

def arpping(host):
	try:
		ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host),timeout=2)
		for s,r in ans:
			if not macExists(r.src):
				print "Unknown MAC Address Detected: " + r.src + " IP Address: " + r.psrc
				q = raw_input("Would you like to add to the list of known MAC's? (Y/n)")
				if (q != "n"):
					print("ADDING MAC " + r.src)
					addMac(r.src)

	except Exception, e:
		print e

def main():
	while True:
		arpping(IP_RANGE)
		time.sleep(T_SLEEP)


if __name__ == '__main__':
	main()

