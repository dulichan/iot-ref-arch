from core.Manager import Manager
class RaspberryPiManager(Manager):
	def generate_challege(self):
		'''
			Generate a challenge token based on a hardware property
		'''
		return '164230d1df67'

	def platform(self):
		return "RaspberryPi"

	def mac(self):
		return "62:03:08:1a:01:00"

	def version(self):
		return "Model B"