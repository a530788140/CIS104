import netifaces

class netState():
	"""
	To obtain target host's pnic and gateway"""
	def __init__(ip, self):
		self.pnic = None
		self.gateway = None
	def pNIC(self):
		self.pnic = netifaces.gateways()['default'][netifaces.AF_INET][1]
