from matplotlib import pyplot as plt
import read_db 
import networkx as nx
import re
import lib.mt
def cycle():
	G = nx.Graph()
	#G.add_edge(1,2)
	#G.add_edge(2,3)
	#G.add_edge(3,4)
	#G.add_edge(3,5)
	#G.add_edge(4,1)
	pair = [(u'ncku-br0', u'patch1-0'), (u'ncku-br1', u'patch0-1'), (u'ncku-br1', u'eth0'), (u'patch0-1', u'patch1-0'), (u'patch0-1', '1'), ('1', 'eth0')]
	G.add_edges_from(pair)
	nx.draw_networkx(G, with_labels=True)
	#plt.show()
	try:
		c = nx.find_cycle(G)
		print c
	except:
		print "No loop"
def ip():
	net = '192.168.163.24/24'
def reg():
	line = 'cats are smarter than dogs here'
	matchObj = re.match( r'(.*) are (.*) .*', line)

	if matchObj:
		print "group", matchObj.group()
		print "group1", matchObj.group(1)
		print "group2", matchObj.group(2)

#cycle()
#reg()
lib.mt.mode()