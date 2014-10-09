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
import commands
import random
class TemperaturePublisher(Process.Process):

    def __init__(self):
        self.com = HttpCommunication.HttpCommunication(
            "http://localhost", 3000)
        pass

    def get_cpu_temp(self):
        tempFile = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = tempFile.read()
        tempFile.close()
        return float(cpu_temp) / 1000
        # Uncomment the next line if you want the temp in Fahrenheit
        # return float(1.8*cpu_temp)+32

    def get_gpu_temp(self):
        gpu_temp = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp').replace(
            'temp=', '').replace('\'C', '')
        return float(gpu_temp)
        # Uncomment the next line if you want the temp in Fahrenheit
        # return float(1.8* gpu_temp)+32

    def run(self):
        '''
                Main task of the Process. This is used to read perform some
                device operations to collect data
        '''
        input = {
            "event": {
                "payloadData": {
                    "tenantId": "100",
                    "deviceId": "data4",
                    "temperature": random.randint(0,100)
                }
            }
        }
        self.publish(input)

    def publish(self, input):
        '''
                Publish the data collected!
        '''
        input = json.dumps(input)
        self.com.publish("application/json", input, "http://localhost:9763/endpoints/http/jsonBuilder")
