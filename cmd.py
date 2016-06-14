import matplotlib
# Force matplotlib to not use any Xwindows backend.
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import networkx as nx
import argparse

import lib.topology as topo
import lib.read_db as read_db
import lib.read_net as read_net
import lib.scan as scan



"""
User input ip/port to indentified smoe host with ovs which connected to physical switch.
"""
def parse(): 
	parser = argparse.ArgumentParser(description='''Create Network Topology, -s -d or -n -i -p
													''')
	parser.add_argument("--scan", help='scan lan network')
	parser.add_argument("-s", "--src", help="add source host ")
 	parser.add_argument("-d", "--dst", help="add destination host")

 	parser.add_argument("-n", "--name", help="Username@IP, for ssh connection")
 	parser.add_argument("-i", "--ip", help="Host IP")
 	parser.add_argument("-p", "--port", type=int, help="Host Port")

 	parser.add_argument("-t","--topology",action='store_true', help="show network topology")

 	parser.add_argument("-l", "--loop", action='store_true', help="network looping detection", default=1)


 	pairList = []
 	br = []
 	port = []
 	pnic = []
	nt = topo.TPG()

	while True:
		cmd = raw_input(">>")
		args = parser.parse_args(cmd.split())
		if args.scan:
			sc = scan.scan(args.scan)
			sc.iprange()

		if args.src and args.dst:
			pairList.append([(args.src, args.dst)])
			continue

		elif args.ip and args.port or args.name:
			"""
			net = read_net.netState(args.name+"@"+args.ip)
			result = net.sshConnect()
			hostname = result[0]
			pnic = result[1:]
			"""
			ovs = read_db.ovsState(args.ip, args.port)

			ovs.dbConnect()
			ovs.interfaceState()
			ovs.portState()
			ovs.bridgeState()
			p = ovs.pair()
			br = ovs.brName
			port = ovs.portName
			#pnic = ovs.pnic

			pairList.append(p)

			#print " %s's ssh connection is completed" %(args.name)

			continue

		elif args.topology:
			nt.addNodes(br, port, pnic)
			[nt.generator(n) for n in pairList]
			#print br, port, pnic
			nt.show()

		elif args.loop:
			nt.addNodes(br, port, pnic)
			[nt.generator(n) for n in pairList]
			try:
				c = nx.find_cycle(nt.G)
				print "Cycle Found!\n Here's the path: ", c
				nt.drawPath(c)
			except:
				print "NO Cycle Found!"
		

def main():
	parse()

if __name__ == '__main__':
	main()