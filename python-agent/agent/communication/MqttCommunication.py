import paho.mqtt.client as mqtt
class MqttCommunication:

	def on_connect(client, userdata, rc):
		print("Connected with result code "+str(rc))
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		client.subscribe("$SYS/#")

	# The callback for when a PUBLISH message is received from the server.
	def on_message(client, userdata, msg):
		print(msg.topic+" "+str(msg.payload))

	def __init__(self, host="localhost", port=1883, on_connect=on_connect, on_message=on_message):
		#self.host = host
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message
		print host
		self.client.connect(host, 1883, 60)

	def publish(self, topic, qos, input):
	#def publish(self):	
		self.client.publish(topic, payload=input, qos=qos)

	