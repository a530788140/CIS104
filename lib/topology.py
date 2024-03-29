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
			cycle = cycle.replace('],','],\n')
			plt.title('Network Topology - ' + 'Cycle found:\n ' + cycle, fontsize=11)
		else:
			plt.title('Network Topology - ' + 'No cycle')
		plt.axis('off')
		#save figure to path
		plt.savefig('/home/hsnet/Desktop/foo.png')
		plt.show()


if __name__ == '__main__':
	ovs1 = read_db.ovsState('140.116.163.140', 5000, 'h', ['eth0', 'lo', 'virbr0', 'br1'])
	ovs1.read()
	host1 = TPG()
	host1.addNodes(ovs1.brName, ovs1.portName)
	host1.generator(ovs1.brPort)
	host1.show('PATH')
