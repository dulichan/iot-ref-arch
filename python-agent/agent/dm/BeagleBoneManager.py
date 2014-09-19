from core.Manager import Manager
class BeagleBoneManager(Manager):
	def generate_challege(self):
		'''
			Generate a challenge token based on a hardware property
		'''
		return '164230d1df67'

	def platform(self):
		return "BeagleBone"

	def mac(self):
		return "62:03:08:1a:01:00"

	def version(self):
		return "10.9.3"

	def properties(self):
		pass