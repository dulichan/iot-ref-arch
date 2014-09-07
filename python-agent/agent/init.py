from Agent import Agent
from custom.TemperaturePublisher import TemperaturePublisher
from custom.HumidityPublisher import HumidityPublisher

from communication.MqttCommunication import MqttCommunication

agent = Agent()
# process = TemperaturePublisher()
# agent.add_process(process)
process = HumidityPublisher()
agent.add_process(process)


#mqtt = MqttCommunication()
agent.execute()

#mqtt.publish("test/iot", 0, "sdfsdf")