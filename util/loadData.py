import json
import sys
import re
import time
import pickle

# Checando se arquivo existe
if(not Path(fn).is_file()):
	print(colored('Erro: Arquivo %s não existe' % fn,'red'))
	sys.exit()

# Ler arquivo de domínios
file = open(fn,'r').read()
r = re.findall('((?:[\w-]+\.)+[a-zA-Z]{2,7})', file)

# Data
domains = list();
		
# Loop por domínios
index = 0
t = time.time()
medio = 0
for dm in r:
	domains.append({"domain": dm, "status": "new"})
	
	# Progresso
	index += 1
	if(((index / r.__len__()) * 100) % .5 == 0):
		print("Processados: %s (%.2f%%)" % (index, (index / r.__len__())*100))
		elapsed_time = time.time() - t
		medio = (medio + elapsed_time)/2
		print("Velocidade: %.2f (Média: %.2f)" % (elapsed_time, medio))
		t = time.time()

# Binary File
with open('data.bin', 'wb') as f:
	pickle.dump(domains, f)		

# # JSON File
# with open('data.json', 'w') as f:
# 	json.dump(domains,f)