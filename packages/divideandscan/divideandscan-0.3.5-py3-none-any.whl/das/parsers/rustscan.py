import ast

from das.parsers import IAddPortscanOutput


class AddPortscanOutput(IAddPortscanOutput):
	"""Child class for processing RustScan output."""

	def parse(self):
		"""
		RustScan raw output parser.

		:return: a pair of values (portscan raw output filename, number of hosts added to DB)
		:rtype: tuple
		"""
		hosts = set()
		for line in self.portscan_raw:
			try:
				ip, ports = line.split(' -> ')
			except Exception:
				pass
			else:
				for port in ast.literal_eval(ports):
					item = {'ip': ip, 'port': port, 'domains': []}
					if item not in self.db:
						self.db.insert(item)

				hosts.add(ip)

		return (self.portscan_out, len(hosts))
