from Agent import Agent
import os
import glob
import pkgutil
import sys
import argparse
import platform
#from custom.TemperaturePublisher import TemperaturePublisher
#from custom.HumidityPublisher import HumidityPublisher

from communication.MqttCommunication import MqttCommunication

agent = Agent()

# Parse command line arguments for the token
parser = argparse.ArgumentParser()
parser.add_argument("--token")
args = parser.parse_args()

# if the token doesn't exists - ask the agent to enroll the device
if(args.token):
   agent.enroll(args.token)
   pass

# agent.execute()