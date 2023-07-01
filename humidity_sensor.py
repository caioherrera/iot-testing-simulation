from gpio import *
from time import *
from environment import *
from physical import *
from pyjs import *
import math

# User added
from specs import specs
import random

ENVIRONMENT_NAME = "Ambient Humidity"
SENSOR_NAME = "humidity_sensor"
SENSOR_SPECS = specs[SENSOR_NAME]
PORT = A0

def main():
	random.seed(time())
	while True:
		loop()
		
def loop():
	global SENSOR_SPECS

	percentage = random.uniform(0.0, 1.0)
	parity = random.randint(0, 1)

	if percentage <= SENSOR_SPECS["expected_readings_freq"]:
		min_value = SENSOR_SPECS["expected_min_value"]
		max_value = SENSOR_SPECS["expected_max_value"]
	elif parity == 1:
		min_value = SENSOR_SPECS["default_min_value"]
		max_value = SENSOR_SPECS["expected_min_value"]
	else:
		min_value = SENSOR_SPECS["expected_max_value"]
		max_value = SENSOR_SPECS["default_max_value"]

	value = random.uniform(min_value, max_value)

	setDeviceProperty(getName(), "level", value)
	value = math.floor(js_map(value, 
		SENSOR_SPECS["default_min_value"], 
		SENSOR_SPECS["default_max_value"], 0, 255))

	analogWrite(PORT, value)
	delay(SENSOR_SPECS["readings_delay_ms"])

if __name__ == "__main__":
	main()