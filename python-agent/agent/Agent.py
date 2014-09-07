from core.Process import Process
import time, threading, ConfigParser


class Agent:

	process_list = []

	def __init__(self):
		self.Config = ConfigParser.ConfigParser()
		self.Config.read("config.conf")
		
		print str(self.Config.get('agent', 'timer'))
		pass

	def add_process(self, process):
		self.process_list.append(process)
		print "Adding process"

	def execute(self):
		'''
		The execution will 
		'''
		#print len(self.process_list)
		for process in self.process_list:
			print "Executing process"
			process.run()

		#threading.Timer(10, self.execute).start()