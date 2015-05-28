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
import paho.mqtt.client as mqtt
class MqttCommunication:

	def on_connect(client, userdata, rc):
		print("Connected with result code "+str(rc))
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		client.subscribe("$SYS/#")

	def __init__(self, host="localhost", port=1883, mqttResponder=MqttResponder(), on_connect=on_connect):
		#self.host = host
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = mqttResponder.on_message
		self.client.connect(host, 1883, 60)

	def publish(self, topic, qos, input):
		self.client.publish(topic, payload=input, qos=qos)

class MqttResponder:
	# The callback for when a PUBLISH message is received from the server.
	def on_message(client, userdata, msg):
		print(msg.topic+" "+str(msg.payload))	
	