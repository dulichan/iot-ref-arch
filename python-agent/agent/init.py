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
parser.add_argument("--dmURL")
#args.token = "sdfsdf"
args = parser.parse_args()
# if the token doesn't exists - ask the agent to enroll the device
if(args.token):
	agent.enroll(args.token)

if(args.dmURL):
	agent.dmURL = args.dmURL
else:
	agent.dmURL = "https://localhost:9443/"

# agent.execute()