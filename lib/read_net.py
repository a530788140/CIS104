import netifaces
import subprocess
import sys

class netState():
	"""
	To obtain target host's pnic and gateway"""
	def __init__(self, host):
		self.host = host
	def sshConnect(self):
		command = "hostname; ls /sys/class/net"
		ssh = subprocess.Popen(["ssh", "%s" % self.host, command],
								shell=False,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE)
		result = ssh.stdout.readlines()
		result = [n.strip('\n') for n in result]
		return result

if __name__ == '__main__':
	
	
	net = netState("hsnet@140.116.163.140")
	r = net.sshConnect()
	s = time.time()
	hostname = r[0]
	pnic = r[1:]
	e = time.time()

	