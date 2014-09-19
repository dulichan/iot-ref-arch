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