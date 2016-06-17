from matplotlib import pyplot as plt
import read_db 
import networkx as nx



class TPG():
	def __init__(self):
		self.G = nx.Graph()


	def addNodes(self, br, port, pnic=None):
		self.br = br
		self.port = port
		#self.pnic = [n for n in pnic if n in self.br]

	def generator(self, pair):
		self.G.add_edges_from(pair)

	def show(self, cycle=None):
		pos = nx.spring_layout(self.G)
		nx.draw_networkx(self.G,pos,with_labels=True)
		nx.draw_networkx_nodes(self.G, pos, nodelist=self.br, node_color='dodgerblue')
		nx.draw_networkx_nodes(self.G, pos, nodelist=self.port, node_color='lawngreen')
		if cycle:
			plt.title('Network Topology\n' + 'Cycle found: ' + cycle)
		else:
			plt.title('Network Topology\n' + 'No cycle')
		plt.axis('off')
		plt.savefig('/home/hsnet/Desktop/foo.png')
		plt.show()


if __name__ == '__main__':
	ovs1 = read_db.ovsState('140.116.163.140', 5000, 'h', ['eth0', 'lo', 'virbr0', 'br1'])
	ovs1.dbConnect()
	ovs1.interfaceState()
	ovs1.portState()
	ovs1.bridgeState()
	br2port = ovs1.pair()
	host1 = TPG()
	host1.addNodes(ovs1.brName, ovs1.portName)
	host1.generator(br2port)
	host1.show('PATH')
