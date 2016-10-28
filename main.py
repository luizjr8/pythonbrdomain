#!/usr/bin/env python
# Author: luizjr8 <luiz@lzjr.com.br>
# A simple python app to parse a list of domains and check if it is available
import re
import whois
import sys
from pathlib import Path
from termcolor import colored

class DomainChecker:
	avail = set();
	taken = set();

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
			wr = whois.whois(dm)
			if(wr.country == None):
				print("%s Domínio %s disponível." % (colored('✓', 'green', attrs=['bold']), colored(dm, 'green')))
				self.avail.add(dm)
			else:
				print("%s Domínio %s registrado por %s" % (colored('✗', 'red', attrs=['bold']), colored(dm,'red'),colored(wr.owner,'red')))
				self.taken.add(dm)

		open('res_avail.txt','w').write('\n'.join(str(e) for e in self.avail))
		open('res_taken.txt','w').write('\n'.join(str(e) for e in self.taken))

# Iniciando
dc = DomainChecker(sys.argv[1])