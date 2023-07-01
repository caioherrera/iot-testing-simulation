from gpio import *
from time import *
from specs import specs
from custom_queue import CustomQueue
from pyjs import *
import mqtt_adapter
import message_helper

TEMPERATURE_SENSOR = {
	"name": "temperature_sensor",
	"port": A0,
	"specs": specs["temperature_sensor"],
	"data": CustomQueue(10)
}

HUMIDITY_SENSOR = {
	"name": "humidity_sensor",
	"port": A1,
	"specs": specs["humidity_sensor"],
	"data": CustomQueue(10)
}

SENSOR_LIST = [TEMPERATURE_SENSOR, HUMIDITY_SENSOR]
logs = CustomQueue(100)

def sut_log(message):
	print(message)

def load_sensor_specs():
	
	global SENSOR_LIST

	for sensor in SENSOR_LIST:
		sensor["specs"] = specs[sensor["name"]]

def read_from_sensor(sensor):
	return analogRead(sensor["port"])

def get_sensor_from_name(name):
	global SENSOR_LIST
	return filter(lambda x: x["name"] == name, SENSOR_LIST)[0]

def read_real_value_from_analog_sensor(sensor):
	return js_map(read_from_sensor(sensor), 0.0, 1023.0, sensor["specs"]["default_min_value"], sensor["specs"]["default_max_value"])

def store_new_data_on_sensor(sensor, value):
	sensor["data"].push(value)

def flush_sensor(sensor):
	return sensor["data"].flush()

def compute_without_inputs(sensor):

	global TEMPERATURE_SENSOR

	if sensor['name'] == TEMPERATURE_SENSOR['name']:
		value_c = read_real_value_from_analog_sensor(sensor)
		value_f = value_c * 1.8 + 32.0
		value_k = value_c + 273.15
		return [value_c, value_f, value_k]
	else:
		values = flush_sensor(sensor)
		if len(values) == 0:
			return [values, None]
		else:
			return [values, sum(values) / len(values)]

def compute_with_inputs(sensor, data_input):

	global TEMPERATURE_SENSOR

	if sensor['name'] == TEMPERATURE_SENSOR['name']:
		value_c = data_input
		value_f = value_c * 1.8 + 32.0
		value_k = value_c + 273.15
		return [value_f, value_k]
	else:
		values = data_input
		if len(values) == 0:
			return None
		else:
			return float(sum(values)) / len(values)

def on_request_received(status, msg, packet):

	sut_log("Detected new message: " + msg)
	
	message = message_helper.decode_message(packet['payload'])
	sut_log(message)

	sensor = get_sensor_from_name(message['target'])
	if message['operation'] == 'read':
		result = read_real_value_from_analog_sensor(sensor)
	elif message['operation'] == 'flush':
		result = flush_sensor(sensor)
	elif message['operation'] == 'compute':
		if 'data_input' in message.keys():
			result = compute_with_inputs(sensor, message['data_input'])
		else:
			result = compute_without_inputs(sensor)

	to_be_published = message_helper.build_message_response(message['id'], result)
	sut_log(to_be_published)
	mqtt_adapter.publish_to_responses(to_be_published)

def main():

	global SENSOR_LIST

	load_sensor_specs()
	mqtt_adapter.setup('IOT') #log_filename)
	mqtt_adapter.setOnMessageReceived(on_request_received)
	
	while True:

		for sensor in SENSOR_LIST:
			value = read_real_value_from_analog_sensor(sensor)
			store_new_data_on_sensor(sensor, value)
		
		sleep(1)

if __name__ == "__main__":
	main()