import matplotlib
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import networkx as nx
import re

import lib.topology as topo
import lib.read_db as read_db
import lib.read_net as read_net


"""
Reading file to execute loop detection
"""

def fileParse():
	"Here's some cmd from file"
	with open('setup.txt', 'r') as f:
		lines = f.readlines()
		cmd = [n.strip('\n').split() for n in lines]
	return cmd

def main(cmd):
	pairList = []
 	br = []
 	port = []
 	pnic = []
	nt = topo.TPG()

	for n in cmd:
		if n[0] == '-a':
			ovs = read_db.ovsState(n[1], int(n[2]))
			ovs.dbConnect()
			ovs.interfaceState()
			ovs.portState()
			ovs.bridgeState()
			p = ovs.pair()
			br.extend(ovs.brName)
			port.extend(ovs.portName)
			pairList.append(p)
		if n[0] == '-s':
			pairList.append([(n[1], n[3])])

	nt.addNodes(br, port, pnic)
	[nt.generator(n) for n in pairList]
	c = nx.find_cycle(nt.G)
	nt.show(str(c).strip('[]'))


if __name__ == '__main__':
	cmd = fileParse()
	main(cmd)
