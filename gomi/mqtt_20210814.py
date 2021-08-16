#! /usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
from datetime import datetime

class aws_mqtt:
	myAWSIoTMQTTClient = None

	def __init__(self, \
				mode = 'publish', \
				host = None,\
				rootCAPath = 'root-CA.crt',\
				certificatePath = 'Thing.cert.pem',\
				privateKeyPath = 'Thing.private.key',\
				port = 443,\
				useWebsocket = False,\
				clientId = 'basicPubSub',\
				topic = None):
		self.mode = mode
		self.host = host 
		self.rootCAPath = rootCAPath
		self.certificatePath = certificatePath
		self.privateKeyPath = privateKeyPath
		self.port = port
		self.useWebsocket = useWebsocket
		self.clientId = clientId
		self.topic = topic

		#check arguments
		if self.mode not in  ['both', 'publish', 'subscribe']:
			print("Unknown mode option %s"  %self.mode)
			exit(2)
		if self.useWebsocket and self.certificatePath and self.privateKeyPath:
			print("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
			exit(2)
		if not self.useWebsocket and (not self.certificatePath or not self.privateKeyPath):
			print("Missing credentials for authentication.")
			exit(2)

		# Port defaults
		if self.useWebsocket and not self.port:  # When no port override for WebSocket, default to 443
			self.port = 443
		if not self.useWebsocket and not self.port:  # When no port override for non-WebSocket, default to 8883
			self.port = 8883
	
		# Init AWSIoTMQTTClient
		if useWebsocket:
			self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
			self.myAWSIoTMQTTClient.configureEndpoint(host, port)
			self.myAWSIoTMQTTClient.configureCredentials(rootCAPath)
		else:
			self.myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
			self.myAWSIoTMQTTClient.configureEndpoint(host, port)
			self.myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

		# AWSIoTMQTTClient connection configuration
		self.myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		self.myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
		self.myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
		self.myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

	# Custom MQTT message callback
	def customCallback(client, userdata, message):
		print("Received a new message: ")
		print(message.payload)
		print("from topic: ")
		print(message.topic)
		print("--------------\n\n")
		exit(2)

	# Configure logging
	def logging(self):
		logger = logging.getLogger("AWSIoTPythonSDK.core")
		logger.setLevel(logging.DEBUG)
		streamHandler = logging.StreamHandler()
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		streamHandler.setFormatter(formatter)
		logger.addHandler(streamHandler)

	# Connect and subscribe to AWS IoT
	def connect(self):
		self.myAWSIoTMQTTClient.connect()
		if self.mode == 'both' or self.mode == 'subscribe':
			self.myAWSIoTMQTTClient.subscribe(self.topic, 1, self.customCallback)
			time.sleep(2)

	#  publish to AWS IoT
	def publish(self,messages='default messages'):
		if self.mode == 'both' or self.mode == 'publish':
			self.myAWSIoTMQTTClient.publish(self.topic, messages, 1)
			print('Published topic %s: %s\n' % (self.topic, messages))
			time.sleep(1)

if __name__ == '__main__':
	try:
		m=aws_mqtt(host = 'a287p9vwxu3415-ats.iot.us-east-2.amazonaws.com',topic = 'iot/topic')
		m.connect()

		msg={}
		msg['text_data'] = "test message"
		msg['numeric_data'] = 9997
		msg['timestamp'] = datetime.now().isoformat(timespec='seconds')
		messageJson = json.dumps(msg)
		
		m.publish(messageJson)
		time.sleep(5)

	except KeyboardInterrupt:
		print('Interruted')