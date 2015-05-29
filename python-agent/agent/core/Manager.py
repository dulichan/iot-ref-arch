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
import requests
import json
import platform
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
# Regarding [Errno 8] _ssl.c:507: EOF occurred in violation of protocol
#http://stackoverflow.com/questions/29134512/insecureplatformwarning-a-true-sslcontext-object-is-not-available-this-prevent 
class Manager:

    '''
            The Core Manager is responsible for managing platform indepenant management tasks
            also the core manager switches the manager based on the platform type
    '''

    def is_enrolled(self, agent):
        '''
            Responsible for finding if the device has been enrolled to the DM
        '''
        return agent.Config.get('agent', 'enrollment')

    def configure_dm_url(self, dm_url):
        '''
        Setup the device Management url     
        '''
        self.dm_url = dm_url

    def enroll(self, agent, token=None):
        '''
                Enrollment process for Device involves calling an API of a server through HTTP
                passing the token. At this time a challenge token will be generated based on hardware.
        '''
        challenge = self.generate_challege()
        properties = self.flatten_device_info(self.device_info())
        properties["Platform"] = self.platform()
        properties["Version"] = self.version()
        properties["Serial"] = self.device_id()
        prop_list = []
        for key, value in properties.iteritems():
            temp = {"name": key, "value": value}
            prop_list.append(temp)

        payload = {
            "deviceIdentifier": self.device_id(),
            "properties": prop_list
        };
        # payload = {
        #     "auth": "token",
        #     "auth_params": {},
        #     "properties": properties
        # }
        # Add the token to payload if token is available
        #if(token != None):
            #print "Token found. Starting token based enrollment <!!!>"
            #payload['auth_params']['token'] = token
        #else:
        print "Token not found. Starting self enrollment <!!!>"
        

        payload = json.dumps(payload)
        headers = {'Content-Type': "application/json", 'Accept': "application/json"}
        url = self.dm_url + "temp-controller-agentr/enrollment/enroll"
        print "URL <--->"
        print url
        print "URL End <***>"
        print "Payload <--->"
        print payload
        print "Payload End <***>"
        response = requests.post(
            url, headers=headers, data=payload, verify=False)
        print "Response <--->"
        #print response.text
        print "Response End <***>"
        if(response.status_code==200):
            #response = json.loads(response.text)
            #self.set_tokens(agent, response["payload"]["tokens"]["access_token"], response[
                             #"payload"]["tokens"]["refresh_token"])
            self.set_tokens(agent)
        else:
            print "Error!!!"

    def set_tokens(self, agent):
        agent.config.set('agent', 'enroll', True)
        #agent.config.set(
            #'agent', 'access_token', access_token)
        #agent.config.set('agent', 'refresh_token', refresh_token)
        with open('config.conf', 'w') as f:
            agent.config.write(f)
    def device_properties(self):
        '''
            Device Properties are sent to the Device Manager in each monitoring interval 
        '''
        info = {
            "mac": self.mac()
        }
        return info

    def flatten_device_info(self, device_info):
        '''
            Currently the server side is not robust to display rich information obtained from different types of devices.
            This method flattens the device info. 
        '''
        props = {
            "Python Version": device_info["python_info"]["version"],
            "Python Compiler": device_info["python_info"]["compiler"],
            "Python Build Name": device_info["python_info"]["build"][0],
            "Python Build Date": device_info["python_info"]["build"][1],
            "Kernal Name": device_info["platform"]["normal"],
            "Platform Name": platform_name(),
            "Node": device_info["hardware"]["node"],
            "System": device_info["hardware"]["system"],
            "Machine": device_info["hardware"]["machine"]
        }
        return props

    def device_info(self):
        '''
            Device Info is sent only when the device is getting registered to the Device Manager. This
            method should be used to send the static information about the device. Device Manager can 
            decide to invoke this method from server side if needed
        '''
        props = {
            "python_info": {
                "version": platform.python_version(),
                "version_tuple": platform.python_version_tuple(),
                "compiler": platform.python_compiler(),
                "build": platform.python_build()
            },
            "platform": {
                "normal": platform.platform(),
                "alias": platform.platform(aliased=True),
                "terse": platform.platform(terse=True)
            },
            "os": {
                "name": platform.uname()
            },
            "hardware": {
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
        }
        return props


def platform_name():
    '''
    The logic of getting the second index item from uname() is incorrect in Mac
    '''
    return platform.uname()[1]


def get_device_manager():
    '''
        TODO: Obtain the device type bundles by reading the dm module. 
    '''
    platform = platform_name()
    platform = "raspberrypi"
    if platform == "raspberrypi":
        return RaspberryPiManager()
    elif platform == "beaglebone":
        return BeagleBoneManager()
    return None
# Avoiding circular depenency [refer -
# http://effbot.org/zone/import-confusion.htm]
from dm.RaspberryPiManager import RaspberryPiManager
from dm.BeagleBoneManager import BeagleBoneManager
