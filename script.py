import fileinput
import re
from datetime import datetime
from heapq import heappush, heappop
import os
import threading

period = 10

def reload():
	threading.Timer(10, reload).start()
	table = {}
	now = datetime.now()
	for line in reversed(list(open("/home/stweb/logs/access.log"))):
		record = line.rstrip()
		time = ""
		response = ""
		request=""
		byte=""
		match = re.match('\[.*\]',record)
		if match:
			time = (match.group())[1:-1]
			time = datetime.strptime(time,'%d/%b/%Y:%H:%M:%S %z')
			time = time.replace(tzinfo=None)
			record = record[match.end():]
		if((now -time).total_seconds() >period):
			break 
		response = record[2:5]
		record = record[5:]
		start = 0
		flag = False
		end = 0
		for i in range(0,len(record)):
			if(start==0 and record[i]=='/'):
				start = i
			elif(start!=0 and (record[i] in ['/',' '])):
				end = i
				break
			elif(start!=0 and record[i]=='.'):
				flag = True
		if(flag):
			request='index'
		else:
			request=record[start+1:end]
		record=record[end:]
		match = re.match('.*"',record)
		if match:
			byte = (record[match.end():])
		if not (request in table):
			table[request]={'2xx':0,'3xx':0,'4xx':0,'5xx':0,'byte':0}
		table[request][response[0]+'xx']+=1
		table[request]['byte']+=int(byte)
		#print(str(time) +' '+ str(response) + ' '+str(request) +' '+ str(byte))

	print('Request\t\t\t2xx\t3xx\t4xx\t5xx\tbyte')
	for request in table:
		print(request+'\t\t\t',end='')
		for key in ['2xx','3xx','4xx','5xx','byte']:
			print(table[request][key],end='\t')
		print()

	current = {}
	for line in open('/etc/nginx/nginx.conf','r'):
		match = re.match('(.*)limit_req_zone \$binary_remote_addr zone=(.*):(.*) rate=(.*)r/s;',line)
		if match:
			# print(match.group(2),match.group(4))
			current[match.group(2)] = int(match.group(4))

	updated = {}
	heap = []
	# print(current)
	for key in current:
		current[key] = 1000
		updated[key] = 1000
		if not key in table:
			table[key]={'2xx':0,'3xx':0,'4xx':0,'5xx':0,'byte':0}
		# print (key, table[key]['2xx'], table[key]['5xx'])
		if table[key]['5xx'] > 0:
			heappush(heap, (-table[key]['5xx'], key))

	margin = 5
	# print(heap)
	for key in current:
		if len(heap) == 0:
			break
		if current[key] - table[key]['2xx'] - margin > 0 and len(heap) > 0:
			excess = current[key] - table[key]['2xx'] - margin
			x = heappop(heap)
			need = -x[0]
			while excess >= need:
				excess = excess - need
				updated[x[1]] = updated[x[1]] + need
				updated[key] = updated[key] - need
				if len(heap) == 0 or excess == 0:
					break
				x = heappop(heap)
				need = -x[0]
			if len(heap) == 0 or excess == 0:
				break
			tmp = -x[0] - excess
			updated[x[1]] = updated[x[1]] + excess
			updated[key] = updated[key] - excess
			heappush(heap, (-tmp, x[1]))

	for key in updated:
		print (key, updated[key])

	for key in updated:
		updated[key] = str((updated[key]))
	#Change nginx file path here
	with fileinput.FileInput('/etc/nginx/nginx.conf', inplace=True) as file:
		for line in file:
			match = re.match('(.*)limit_req_zone \$binary_remote_addr zone=(.*):(.*) rate=(.*);',line)
			if match:
				line = '\tlimit_req_zone $binary_remote_addr zone='+match.group(2)+':'+match.group(3)+' rate='+updated[match.group(2)]+'r/s;\n'
			print(line,end='')
	#Gracefully Reload Nginx with the new config
	print("Reloading Nginx")
	os.system("sudo nginx -s reload");
	#sudoPassword = 'STW@1234#'
	#command = 'nginx -s reload'
	#p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

#def printit():
  #threading.Timer(1.0, printit).start()
  #print("Hello, World!")

#printit()
reload()

