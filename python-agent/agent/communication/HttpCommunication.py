import unirest

class HttpCommunication:

	def __init__(self, host="http://localhost", port=80):
		self.host = host
		self.port = port

	def callback_function(response):
  		response.code # The HTTP status code
  		response.headers # The HTTP headers
  		response.body # The parsed response
  		response.raw_body # The unparsed response


	def publish(self, endpoint, data_type, input):
		payload = input
		headers = {'content-type': data_type}
		endpoint = self.host+":"+str(self.port)+"/"+endpoint
		thread = unirest.post(endpoint, params=payload, headers=headers, callback=self.callback_function)
		pass
