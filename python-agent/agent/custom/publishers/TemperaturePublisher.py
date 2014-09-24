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
from core import Process
from communication import HttpCommunication
import json

class TemperaturePublisher(Process.Process):
	def __init__(self):
		self.com = HttpCommunication.HttpCommunication("http://localhost", 3000)
		pass

	def run(self):
		'''
			Main task of the Process. This is used to read perform some 
			device operations to collect data
		'''
		input = {"temperature": 20}
		self.publish(input)

	def publish(self, input):
		''' 
			Publish the data collected!
		'''
		input = json.dumps(input)
		self.com.publish("temperature", "application/json", input)