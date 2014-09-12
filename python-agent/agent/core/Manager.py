import requests
import json
class Manager:
	'''
		The Core Manager is responsible for managing platform indepenant management tasks
		also the core manager switches the manager based on the platform type
	'''
	def enroll(self, token):
		'''
			Enrollment process for Device involves calling an API of a server through HTTP 
			passing the token. At this time a challenge token will be generated based on hardware. 
		'''
		challenge = self.generate_challege()
		payload = {'token':token, 'platform':self.platform()}
		payload = json.dumps(payload)
		headers = {'content-type': "application/json"}
		response = requests.post("http://localhost:3000/register",headers=headers, data=payload)
		print response.text
		pass