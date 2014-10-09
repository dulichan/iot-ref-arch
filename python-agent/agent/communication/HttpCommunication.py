'''
	Copyright (c) 2005-2011, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.

	WSO2 Inc. licenses this file to you under the Apache License,
	Version 2.0 (the "License"); you may not use this file except
	in compliance with the License.
	You may obtain a copy of the License at

		http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing,
	software distributed under the License is distributed on an
	"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
	KIND, either express or implied.  See the License for the
	specific language governing permissions and limitations
	under the License.
'''
import unirest

class HttpCommunication:

	def __init__(self, host="http://localhost", port=80):
		self.host = host
		self.port = port
		self.endpoint = self.host+":"+str(self.port)

	def callback_function(self, response):
  		response.code # The HTTP status code
  		response.headers # The HTTP headers
  		response.body # The parsed response
  		response.raw_body # The unparsed response
  		print response.code

	def publish(self, data_type, input, endpoint):
		payload = input
		headers = {'content-type': data_type}
		thread = unirest.post(endpoint, params=payload, headers=headers, callback=self.callback_function)
		pass
