import json
import sys
import re
import time
import pickle
from enum import Enum
# Data

# States
class States(Enum):
	NEW = "new"
	TAKEN = "taken"
	LOCKED = "locked"
	WAITING = "waiting"
	AVAIL = "avail"
	ERROR = "error"	

# print()
class DomainsBase():
	domains = list()
	file = "data.bin"


	def __init__(self, file="data.bin"):
		self.file = file
		with open(file, 'rb') as f:
			self.domains = pickle.load(f)	
			# self.__init_data()

	def exists(self, domain):
		return self.getDomain(domain) != None

	def getDomain(self, domain):
		obj = [x for x in self.domains if x['domain'] == domain]
		if(len(obj) > 0):
			return obj[0]

	def getDomains(self, state):
		obj = [x for x in self.domains if 'status' in x.keys() and x['status'] == state.value]
		if(len(obj) > 0):
			return obj

	def setState(self, domain, state):
		obj = self.getDomain(domain)
		if(obj != None):
			obj['status'] = state.value
			self.__changedDomain(domain)

	def setError(self, domain, error):
		obj = self.getDomain(domain)
		if(obj != None):
			obj['status'] = States.ERROR.value
			obj['error'] = error
			self.__changedDomain(domain)

	def __changedDomain(self, domain):
		obj = self.getDomain(domain)
		if(obj != None):
			obj['changedAt'] = time.strftime('%Y-%m-%dT%H:%M:%S')

	def addDomain(self, domain):
		if(not self.exists(domain)):
			domains.append({'domain': domain})
			self.setState(domain, States.NEW)
			self.__changedDomain(domain)

	def save(self):
		with open(self.file, 'wb') as f:
			pickle.dump(self.domains, f)	

	def saveJSON(self, filename):
		with open(filename, 'w') as f:
			json.dump(self.domains, f)	