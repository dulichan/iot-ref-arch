import core.Manager as Manager
import time
import threading
import ConfigParser
import os
import pkgutil
import sys


class Agent:

    process_list = []

    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.Config.read("config.conf")
        self.timer = self.Config.get('agent', 'timer')
        print self.timer
        self.timer_interval = float(self.Config.get('agent', 'timer_interval'))
        self.autoload = self.Config.get('agent', 'autoload')

        # Load the manager based on the board
        self.load_manager()

    def load_manager(self):
        #self.manager = RaspberryPiManager()
        self.manager = Manager.get_device_manager()

    def enroll(self, token):
        self.manager.enroll(token)

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

        if self.autoload == 'True':
            self.reload()

        if self.timer == 'True':
            threading.Timer(self.timer_interval, self.execute).start()

    def reload(self):
        '''
        Reload processors
        '''
        path = os.path.join(os.path.dirname(__file__), "custom/publishers")
        modules = pkgutil.iter_modules(path=[path])

        for loader, mod_name, ispkg in modules:
            # Ensure that module isn't already loaded
            # print mod_name not in sys.modules
            if "custom." + mod_name not in sys.modules:
            # Import module
                loaded_mod = __import__(
                    "custom" + "." + mod_name, fromlist=[mod_name])

                # Load class from imported module
                class_name = mod_name
                loaded_class = getattr(loaded_mod, class_name)

                # Create an instance of the class
                instance = loaded_class()
                self.add_process(instance)
