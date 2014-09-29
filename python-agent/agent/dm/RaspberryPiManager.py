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

	def getserial():
		'''
			http://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
		'''
		# Extract serial from cpuinfo file
		cpuserial = "0000000000000000"
		try:
			f = open('/proc/cpuinfo','r')
			for line in f:
				if line[0:6]=='Serial':
					cpuserial = line[10:26]
					f.close()
		except:
			cpuserial = "ERROR000000000"
		return cpuserial