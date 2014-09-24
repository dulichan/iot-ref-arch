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
from core.Process import Process
from communication.MqttCommunication import MqttCommunication
import json

class HumidityPublisher(Process):
	def __init__(self):
		self.com = MqttCommunication()
		pass

	def run(self):
		'''
			Main task of the Process. This is used to read perform some 
			device operations to collect data
		'''
		input = {"humidity": 50}
		self.publish(input)

	def publish(self, input):
		''' 
			Publish the data collected!
		'''
		input = json.dumps(input)
		self.com.publish("rpie/humidity", 0, input)