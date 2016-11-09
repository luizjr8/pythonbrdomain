#!/usr/bin/env python
# Author: luizjr8 <luiz@lzjr.com.br>
# A simple python app to parse a list of domains and check if it is available
import re
import sys
import json
import requests
from pathlib import Path
from termcolor import colored
from DomainBase import DomainsBase, States

class DomainChecker:
	db = DomainsBase()

	def __init__(self, fn="data.bin"):
		print('Iniciando com o banco %s' % fn)
		
		# Loop por domínios
		for dmn in self.db.getDomains(States.NEW):
			# Nome do Domínio
			dm = dmn['domain']
			wr = lambda:None
			try:
				# Requisição Usando isAvail (CGI)
				resp = requests.get(url="https://registro.br/cgi-bin/avail/?qr=%s" % dm, timeout=10)
				wr.__dict__ = json.loads(resp.text)
				
				# Checa se é válido
				if(wr.available):
					print("%s Domínio %s disponível." % (colored('✓', 'green', attrs=['bold']), colored(dm, 'green')))
					self.db.setState(dm, States.AVAIL)
				elif('aguardando' in wr.reason):
					print("%s Domínio %s aguardando próximo processo de liberação." % (colored('◆', 'yellow', attrs=['bold']), colored(dm, 'yellow')))
					self.db.setState(dm, States.WAITING)
				elif('participado' in wr.reason):
					print("%s Domínio %s bloqueado por ter participado de 6 processos." % (colored('⦰', 'grey', attrs=['dark']), colored(dm, 'grey')))
					self.db.setState(dm, States.LOCKED)
				else:
					print("%s Domínio %s já registrado. (%s)" % (colored('✗', 'red', attrs=['bold']), colored(dm,'red'),colored(wr.reason,'red')))
					self.db.setState(dm, States.TAKEN)
			# Sai do loop em caso de ctrl+c
			except KeyboardInterrupt:
				break
			# Continua caso erro comum (rede, timeout, etc)
			except:
				print("Unexpected error:", sys.exc_info()[0])
				self.db.setError(dm, sys.exc_info()[0])
				continue

		# Salva outputs
		self.db.save()
		self.db.saveJSON()
# Iniciando
dc = DomainChecker()