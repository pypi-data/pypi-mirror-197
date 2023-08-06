from user_agent import generate_user_agent
import exceptions


def getUserAgent(userAgentType):
	try:
		return generate_user_agent(device_type=userAgentType)
	except:
		raise exceptions.InvalidUserAgentType(userAgentType)
		
def log(message):
	print(message)
	
def export(data,file):
			if file.split('.')[1] in ['csv','json']:
				if file.split('.')[1] == 'csv':
					from csv import writer
					if type(data[0]) != list:
						data = [[i] for i in data]
					with open(file,'w') as wfile:
						csvFile = writer(wfile)
						csvFile.writerows(data)
						print(f'Exported to file {file}')
				else:
					headers = data[0]
					jsonData = []
					for i in data[1:]:
						i = zip(headers,i)
						buffer = {}
						for j in i:
							buffer[j[0]] = j[1]
						jsonData.append(buffer)
					from json import dump
					with open(file,'w') as wfile:
						dump(jsonData,wfile)
						print(f'Exported to file {file}')
			else:
				raise exceptions.InvalidExportFileFormat(file)