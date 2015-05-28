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
import core.Manager as Manager
from custom.publishers.TemperaturePublisher import TemperaturePublisher
import time
import threading
import ConfigParser
import os
import pkgutil
import sys
import argparse

class Agent:

    def start(self):
        self.load_manager()
        arguments = self.pass_arguments()
        if(arguments.dmURL):
            self.configure_dm_url(arguments.dmURL)
        else:
            self.configure_dm_url("https://localhost:9453/")

        if(arguments.token):
            # if the token doesn't exists - ask the agent to enroll the device
            self.manager.enroll(self, arguments.token)
        else:
            enroll = self.agent_params['enroll']
            if(enroll):            
                print "Device was enrolled to Device Manager previously"
            else:
                self.manager.enroll(self)   
        self.add_process(TemperaturePublisher())
        self.execute()

    def pass_arguments(self):
        '''
            Parse command line arguments for the token
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("--token")
        parser.add_argument("--dmURL")
        args = parser.parse_args()
        # args.token = "sdfsdf"
        return args

    def __init__(self):
        '''
            Parse config files and setup agent variables
        '''
        self.config = ConfigParser.ConfigParser()
        self.config.read("config.conf")

        self.process_list = []
        self.agent_params = {}
        self.configs = {}
        # Runtime configs
        self.agent_params['timer'] = self.config.get('agent', 'timer')
        self.agent_params['timer_interval'] = float(self.config.get('agent', 'timer_interval'))
        self.agent_params['autoload'] = self.config.get('agent', 'autoload')

        self.configs['deviceId'] = device_id()

        # Security code
        if(self.config.has_section('security')):
            self.agent_params['access_token'] = self.config.get('security', 'access_token')
            self.agent_params['refresh_token'] = self.config.get('security', 'refresh_token')
            self.agent_params['enroll'] = self.config.get('security', 'enroll')
        else:
            self.agent_params['enroll'] = False

    def configure_dm_url(self, dm_url):
        self.manager.configure_dm_url(dm_url)

    def load_manager(self):
        '''
            Load the Platform specific Device Manager implementation using the core Device Manager
        '''
        #self.manager = RaspberryPiManager()
        self.manager = Manager.get_device_manager()
        if(self.manager==None):
            raise Exception("No Device Manager found for Platform")

    def add_process(self, process):
        self.process_list.append(process)
        print "Adding process " + str(process)

    def execute(self):
        '''
        The execution will run periodically based on the timer property in
        the config.conf file
        '''
        # print len(self.process_list)
        for process in self.process_list:
            print "Executing process"
            process.run()

        if self.agent_params['autoload'] == 'True':
            self.reload()

        if self.agent_params['timer'] == 'True':
            threading.Timer(self.agent_params['timer_interval'], self.execute).start()

    def reload(self):
        '''
        Reload processors
        '''
        path = os.path.join(os.path.dirname(__file__), "custom/publishers")
        modules = pkgutil.iter_modules(path=[path])

        for loader, mod_name, ispkg in modules:
            # Ensure that module isn't already loaded
            # print mod_name not in sys.modules
            if "custom.publishers." + mod_name not in sys.modules:
            # Import module
                loaded_mod = __import__(
                    "custom.publishers" + "." + mod_name, fromlist=[mod_name])

                # Load class from imported module
                class_name = mod_name
                loaded_class = getattr(loaded_mod, class_name)

                # Create an instance of the class
                instance = loaded_class()
                self.add_process(instance)
