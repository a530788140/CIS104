import re
import socket
import struct
import subprocess

import lib.read_db as read_db
"""
TODO: IP scanner for network loop
"""

class scan():
	def __init__(self, ip):
		self.ip=ip
		self.totalIP = []

	def iprange(self):
		match = re.search(r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\/([0-9]|[1-2][0-9]|3[0-2])$', self.ip)
		if match:
			pass
		else:
			print "Invalid IP format"

		(ip, cidr) = self.ip.split('/')

		ip_bi = ''.join(format(int(x), '08b') for x in ip.split('.'))

		broadcast = ip_bi[:int(cidr)]
		netmask = ip_bi[:int(cidr)]
		
		
		for n in range(int(cidr), len(ip_bi)):
			netmask += '0'
			broadcast += '1'
		#print 'netmask:   {0} \nbroadcast: {1}'.format(netmask, broadcast)

		broadcast = int(broadcast, base=2)
		netmask = int(netmask, base=2)

		self.totalIP = [socket.inet_ntoa(struct.pack('!L', n)) for n in range(netmask, broadcast+1)]
		
		#Checking hosts availability, but it's slow with using socket
		for i in self.totalIP:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print i
			if not s.connect_ex((i, 5000)):
				print "YES"
				host = read_db.ovsState(i ,5000)
				ovs.dbConnect()
				ovs.interfaceState()
				ovs.portState()
				ovs.bridgeState()

				s.close()
			else:
				print "NO"




if __name__ == '__main__':
	host = scan('140.116.163.140/31')
	host.iprange()

