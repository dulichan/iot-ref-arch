from Agent import Agent
import os
import glob
import pkgutil
import sys
#from custom.TemperaturePublisher import TemperaturePublisher
#from custom.HumidityPublisher import HumidityPublisher

from communication.MqttCommunication import MqttCommunication

agent = Agent()

agent.execute()