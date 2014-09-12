from Agent import Agent
import os
import glob
import pkgutil
import sys
import argparse
#from custom.TemperaturePublisher import TemperaturePublisher
#from custom.HumidityPublisher import HumidityPublisher

from communication.MqttCommunication import MqttCommunication

agent = Agent()

# Parse command line arguments for the token
parser = argparse.ArgumentParser()
parser.add_argument("--token")
args = parser.parse_args()

args.token = '9c6c4c7e-39da-11e4-84d8-164230d1df67'
# if the token doesn't exists - ask the agent to enroll the device
if(args.token):
    agent.enroll(args.token)

# agent.execute()
