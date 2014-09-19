import requests
import json
import platform

class Manager:

    '''
            The Core Manager is responsible for managing platform indepenant management tasks
            also the core manager switches the manager based on the platform type
    '''
    def enroll(self, token):
        '''
                Enrollment process for Device involves calling an API of a server through HTTP
                passing the token. At this time a challenge token will be generated based on hardware.
        '''
        challenge = self.generate_challege()
        payload = {
            "auth": "token",
            "auth_params": {
                "token": token
            },
            "properties": {
             	"platform": self.platform(),
             	"version" : self.version(),
                "extra": device_info()
            }
        }

        payload = json.dumps(payload)
        headers = {'content-type': "application/json"}
        print payload
        response = requests.post(
            "https://10.100.0.210:9443/emm/api/devices/iot/register", headers=headers, data=payload, verify=False)
        print response.text

    def device_properties(self):
        '''
            Device Properties are sent to the Device Manager in each monitoring interval 
        '''
        info = {
            "mac": self.mac()
        }
        return info

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
            "platform":{
                "normal": platform.platform(),
                "alias": platform.platform(aliased=True),
                "terse":platform.platform(terse=True)
            },
            "os":{
                "name": platform.uname()
            },
            "hardware":{
                "system": platform.system(),
                "node": platform.node(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor()
            }
        }
        return props