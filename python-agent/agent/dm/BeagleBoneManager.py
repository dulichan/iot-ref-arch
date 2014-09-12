from core.Manager import Manager
class BeagleBoneManager(Manager):
	def generate_challege(self):
		'''
			Generate a challenge token based on a hardware property
		'''
		return '164230d1df67'

	def platform(self):
		return "BeagleBone"