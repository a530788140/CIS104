import read_db 
import networkx as nx
import matplotlib.pyplot as plt

class TPG():
	def __init__(self, db, gateway, host):
		self.db = db
		self.gateway = gateway
		self.host = host
		self.G = nx.Graph()
		self.brPort = []
		self.patchPort = []
	def patch(self):
		for name, value in self.db.items():
			for port in value:
				#Got bridge-Port edge
				n = self.host + '-' + name
				self.brPort.append((n, port[0]))
				if len(port[1][1]) != 0:
					#If port has options
					for n in port[1][1]:
						#Got patch port edge
						self.patchPort.append((port[0], n[1]))
		print self.brPort
		print self.patchPort

	def generator(self):
		self.G.add_edges_from(self.brPort)
		self.G.add_edges_from(self.patchPort)
		nx.draw_networkx(self.G, with_labels=True)
		plt.show()
		
if __name__ == '__main__':
	ovs1 = read_db.ovsState('140.116.163.140', 5000, 'eth0')
	ovs1.dbConnect()
	ovs1.interfaceState()
	ovs1.portState()
	ovs1.bridgeState()
	host1 = TPG(ovs1.brdict, '140.116.163.157', 'hsnet')
	host1.patch()
	host1.generator()