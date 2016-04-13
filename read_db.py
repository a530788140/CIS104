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
	def __init__(self, ip, port, pnic):
		self.ip = ip
		self.port = port
		#TODO ssh get pnic/gw
		self.pnic = pnic
		self.ifacedict = {}
		self.portdict = {}
		self.brdict = collections.defaultdict(list)

	def getPNIC(self):
		nic = ni.interfaces()
		for n in nic:
			connected = subprocess.check_output(['cat',  '/sys/class/net/' + n + '/carrier'])
			connected = int(connected)

			if connected == 1:
				print "Your pnic name is: ", n

	def dbConnect(self):
		"""
		Connect to ovsdb and return conf.db in json format"""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		s.settimeout(8)
		
		try:
			s.connect((self.ip, self.port))

		except socket.error, exc:
			print "Time out , please check ovsdb port setting"
			sys.exit(1)
		
		s.send(db.list_bridges())
		self.ovs_list = db.gather_reply(s)

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

		for key,value in port.items():
			iface_uuid = value['new']['interfaces'][1]
			if iface_uuid not in self.ifacedict.keys():
				continue
			else:
				uuid = key
				name = value['new']['name']
				self.portdict[uuid] = [name, self.ifacedict[iface_uuid]]

	def bridgeState(self):
		bridge = self.ovs_list['result']['Bridge']
		self.brPatchPort = {}
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



	def patchPNIC(self):
		pnicOnBridge = []
		for key, value in self.brdict.items():
			for port in value:
				if port[0] in self.pnic:
					pnicOnBridge.append((key, port[0]))

		return pnicOnBridge

	def patchPort(self):
		#return list of tuples patch port
		patch = []
		interface = self.ovs_list['result']['Interface']
		for key, value in interface.items():
			if value['new']['type'] == 'patch':
				name = value['new']['name']
				options = value['new']['options'][1]
				for n in options:
					if n[0] == 'peer':
						patch.append((name, n[1]))	
		return patch

if __name__ == '__main__':
	ovs1 = ovsState('140.116.163.140', 5000, ['eth0'])
	ovs1.dbConnect()
	ovs1.interfaceState()
	ovs1.portState()
	ovs1.bridgeState()

