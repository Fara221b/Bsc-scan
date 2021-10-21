from Function import fetch_data

contract_address = input('Enter contract address: ')
offest = int(input('Enter number of transaction (default = 1000) : '))
time = int(input('Enter what minuets should be consider after pump (default=1) : '))


data = fetch_data(contract_address,offest,time)

print('Token Name: ',data['Token Name'])
print('Pump time: ',data['pump time'])

if len(data['val'])> 0:
	for vals in data['val']:
		print('val: ',vals)
else:
	print('I cant find val')

if len(data['suspectes'])>0:
	for sus in data['suspectes']:
		print('suspectes : ' ,sus)
else:
	print('I cant find any suspects wallet')

