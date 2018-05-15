#!/usr/bin/python

'''
Requirements:

 python 2.7
 pip install scapy
 
'''

import string, sys, time
from scapy.all import *


conf.verb = 0

IP_RANGE = "10.0.0.1/24"
MAC_ADDR = ["00:00:00:00:00:00","01:01:01:01:01:01"]
T_SLEEP = 30

def arpping(host):
	try:
		ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=host),timeout=2)
		for s,r in ans:
		#	print r.src
			if r.src not in MAC_ADDR:
				print "Unknown MAC Address Detected: " + r.src + " IP Address: " + r.psrc
	except Exception, e:
		print e

def main():
	while True:
		arpping(IP_RANGE)
		time.sleep(T_SLEEP)


if __name__ == '__main__':
	main()
