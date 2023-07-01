import json
import mqttclient
from time import *

MQTT_USERNAME_IOT = "iotsystem"
MQTT_PASSWORD_IOT = "iotsystem"
MQTT_LOG_IOT = "iot-log"

MQTT_USERNAME_TESTER = "tester"
MQTT_PASSWORD_TESTER = "tester"
MQTT_LOG_TESTER = "tester-log"

MQTT_BROKER_ADDRESS = "192.168.1.2"
MQTT_REQUESTS_TOPIC = "REQUESTS"
MQTT_RESPONSES_TOPIC = "RESPONSES"

def mqtt_log_adapter(status, msg, packet):
	if status == "Success" or status == "Error":
		print(status + ": " + msg)
	elif status == "":
		print(msg)

### Connecting functions

def connect(user, pwd):
	global MQTT_BROKER_ADDRESS
	mqttclient.connect(MQTT_BROKER_ADDRESS, user, pwd)

def iot_connect():
	global MQTT_USERNAME_IOT
	global MQTT_PASSWORD_IOT
	connect(MQTT_USERNAME_IOT, MQTT_PASSWORD_IOT)

def tester_connect():
	global MQTT_USERNAME_TESTER
	global MQTT_PASSWORD_TESTER
	connect(MQTT_USERNAME_TESTER, MQTT_PASSWORD_TESTER)

### Subscribing functions

def subscribe(topic):
	mqttclient.subscribe(topic)

def subscribe_to_requests():
	global MQTT_REQUESTS_TOPIC
	subscribe(MQTT_REQUESTS_TOPIC)

def subscribe_to_responses():
	global MQTT_RESPONSES_TOPIC
	subscribe(MQTT_RESPONSES_TOPIC)

### Publishing functions

def publish(topic, payload):
	mqttclient.publish(topic, payload, '0')

def publish_to_requests(payload):
	global MQTT_REQUESTS_TOPIC
	publish(MQTT_REQUESTS_TOPIC, payload)

def publish_to_responses(payload):
	global MQTT_RESPONSES_TOPIC
	publish(MQTT_RESPONSES_TOPIC, payload)

def publish_iot_logs(payload):
	global MQTT_LOG_IOT
	publish(MQTT_LOG_IOT, payload)

def publish_tester_logs(payload):
	global MQTT_LOG_TESTER
	publish(MQTT_LOG_TESTER, payload)

###	Misc functions

def disconnect():
	mqttclient.disconnect()

def setOnMessageReceived(callback):
	mqttclient.onMessageReceived(callback)

def setup(role):

	#global filename
	global MQTT_LOG_IOT
	global MQTT_LOG_TESTER
	
	mqttclient.init()
	mqttclient.onConnect(mqtt_log_adapter)
	mqttclient.onDisconnect(mqtt_log_adapter)
	mqttclient.onSubscribe(mqtt_log_adapter)
	mqttclient.onUnsubscribe(mqtt_log_adapter)
	mqttclient.onPublish(None)

	if role == 'IOT':
		iot_connect()
		delay(500)
		subscribe_to_requests()
		subscribe(MQTT_LOG_IOT)
	else:
		tester_connect()
		delay(500)
		subscribe_to_responses()
		subscribe(MQTT_LOG_TESTER)

