#!/usr/bin/env python
# Author: luizjr8 <luiz@lzjr.com.br>
# A simple python app to parse a list of domains and check if it is available
import re
import sys
import json
import requests
from pathlib import Path
from termcolor import colored

class DomainChecker:
	avail = set();
	taken = set();
	locked = set();
	delayed = set();

	def __init__(self, fn):
		print('Iniciando com o arquivo %s' % fn)
		
		# Checando se arquivo existe
		if(not Path(fn).is_file()):
			print(colored('Erro: Arquivo %s não existe' % fn,'red'))
			sys.exit()
		
		# Abre o arquivo informado e faz o Regex
		file = open(fn,'r').read()
		r = re.findall('((?:[\w-]+\.)+[a-zA-Z]{2,7})', file)
		
		# Loop por domínios
		for dm in r:
			# Try
			try:
				# Requisição Usando isAvail (CGI)
				resp = requests.get(url="https://registro.br/cgi-bin/avail/?qr=%s" % dm, timeout=10)
				wr = lambda:None
				wr.__dict__ = json.loads(resp.text)

				# Checa se é válido
				if(wr.available):
					print("%s Domínio %s disponível." % (colored('✓', 'green', attrs=['bold']), colored(dm, 'green')))
					self.avail.add(dm)
				elif('aguardando' in wr.reason):
					print("%s Domínio %s aguardando próximo processo de liberação." % (colored('◆', 'yellow', attrs=['bold']), colored(dm, 'yellow')))
					self.delayed.add(dm)
				elif('participado' in wr.reason):
					print("%s Domínio %s bloqueado por ter participado de 6 processos." % (colored('⦰', 'grey', attrs=['dark']), colored(dm, 'grey')))
					self.locked.add(dm)
				else:
					print("%s Domínio %s já registrado. (%s)" % (colored('✗', 'red', attrs=['bold']), colored(dm,'red'),colored(wr.reason,'red')))
					self.taken.add(dm)
			except KeyboardInterrupt:
				break
			except:
				print("Unexpected error:", sys.exc_info()[0])
				continue

		open('res_avail.txt','w').write('\n'.join(str(e) for e in self.avail))
		open('res_taken.txt','w').write('\n'.join(str(e) for e in self.taken))
		open('res_delayed.txt','w').write('\n'.join(str(e) for e in self.delayed))
		open('res_locked.txt','w').write('\n'.join(str(e) for e in self.locked))

# Iniciando
dc = DomainChecker(sys.argv[1])