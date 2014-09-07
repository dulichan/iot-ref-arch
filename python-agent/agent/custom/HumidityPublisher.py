from core import Process
from communication.MqttCommunication import MqttCommunication
import json

class HumidityPublisher(Process.Process):
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