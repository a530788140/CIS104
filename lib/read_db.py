import netifaces as ni
import socket
import sys
import json
import collections
import subprocess
import networkx as nx
import matplotlib.pyplot as plt

import ovsdb as db


class ovsState():
	"""
	Got the target host ovsdb/network information"""
	def __init__(self, ip, port, host=None, pnic=None):
		self.ip = ip
		self.port = port
		self.host = host
		self.ifacedict = {}
		self.portdict = {}
		self.brdict = collections.defaultdict(list)
		#self.pnic = [ self.ip+'-'+n for n in pnic]


	def dbConnect(self):
		"""
		Connect to ovsdb and return conf.db in json format"""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.settimeout(1)
		
		try:
			s.connect((self.ip, self.port))

		except socket.error, exc:
			print "Cannot connect to ovsdb, plz check your setting"
			sys.exit(1)
		
		s.send(db.list_bridges())
		self.ovs_list = db.gather_reply(s)
		s.close()

	def interfaceState(self):
		#ifacedict store interface state in format {interface_uuid:{interface_name, options}}
		interface = self.ovs_list['result']['Interface']

		for key,value in interface.items():
			tp = value["new"]["type"]
			#we don't need to consider internal port
			if tp == u"internal":
				continue
			else:
				uuid = key
				name = value['new']['name']
				options = value['new']['options'][1]
				self.ifacedict[uuid] = [name, options]
		

	def portState(self):
		#portdict store port and its interface state in format {port_uuid:{port_name, interface_name, options}}
		port = self.ovs_list['result']['Port']
		self.portName = []

		for key,value in port.items():
			iface_uuid = value['new']['interfaces'][1]
			if iface_uuid not in self.ifacedict.keys():
				continue
			else:
				uuid = key
				name = value['new']['name']
				self.portdict[uuid] = [name, self.ifacedict[iface_uuid]]

		self.portName = [j[0] for i,j in self.portdict.items()]

	def bridgeState(self):
		bridge = self.ovs_list['result']['Bridge']
		self.brPatchPort = {}
		self.brName = []

		for key,value in bridge.items():
			uuid = key
			port_list = value['new']['ports'][1]
			name = value['new']['name']
			for n in port_list:
				port_uuid = n[1]
				if port_uuid not in self.portdict:
					continue
				else:
					#{br:[list of port state]}
					self.brdict[name].append(self.portdict[port_uuid])

		self.brName = [self.ip + '-' + n for n in self.brdict.keys()]

	def pair(self):
		brPort = []
		patchPort = []
		for name, value in self.brdict.items():
			for port in value:
				#Got bridge-Port edge, and specify host name
				n = self.ip + '-' + name
				brPort.append((n, port[0]))
				if len(port[1][1]) != 0:
					#If port has options
					for n in port[1][1]:
						#Got patch port edge 
						#notice: here has some redudant pair:(a,b)=(b,a)
						brPort.append((port[0], n[1]))
		return brPort


if __name__ == '__main__':
	
	ovs1 = ovsState('140.116.163.140', 5000, "hsnet", ['eth0', 'lo', 'virbr0'])
	ovs1.dbConnect()
	ovs1.interfaceState()
	ovs1.portState()
	ovs1.bridgeState()
	print "PNIC: ",ovs1.pnic
	p = ovs1.pair()
	for n in p:
		print n
