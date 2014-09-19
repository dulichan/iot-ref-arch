import requests
import json


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
                "mac": self.mac()
            }
        }

        payload = json.dumps(payload)
        headers = {'content-type': "application/json"}
        response = requests.post(
            "https://localhost:9443/emm/api/devices/iot/register", headers=headers, data=payload, verify=False)
        print response.text
        pass
