import mqtt_adapter
import message_helper
from time import *
from specs import specs
from test_report import TestReport
import random

MAX_ITERATIONS = 50
TEST_ITERATION = 0
EXISTING_TESTS = {}

TEST_ORACLE_TEMPERATURE = [
	[13,55.4,286.15],
	[45,113,318.15],
	[-49,-56.2,224.15],
	[32,89.6,305.15],
	[48,118.4,321.15],
	[35,95,308.15],
	[19,66.2,292.15],
	[12,53.6,285.15],
	[21,69.8,294.15],
	[30,86,303.15],
	[38,100.4,311.15],
	[20,68,293.15],
	[18,64.4,291.15],
	[17,62.6,290.15],
	[41,105.8,314.15],
	[33,91.4,306.15],
	[19,66.2,292.15],
	[19,66.2,292.15],
	[42,107.6,315.15],
	[36,96.8,309.15],
	[14,57.2,287.15],
	[49,120.2,322.15],
	[18,64.4,291.15],
	[23,73.4,296.15],
	[12,53.6,285.15],
	[18,64.4,291.15],
	[-56,-68.8,217.15],
	[28,82.4,301.15]
]

TEST_ORACLE_HUMIDITY = [
	[[], None],
	[[17.0,17.0,38.0],24.0],
	[[26.0,24.0,35.0,24.0,21.0,17.0,27.0,7.0,36.0],24.111111],
	[[30.0,21.0,82.0,40.0,28.0,6.0,35.0,23.0],33.125],
	[[23.0,8.0,8.0,22.0,38.0,33.0,41.0,13.0],23.25],
	[[59.0,13.0,32.0,30.0],33.5],
	[[30.0,16.0,6.0,39.0],22.75],
	[[],None],
	[[26.0],26.0],
	[[8.0,51.0],29.5],
	[[12.0,15.0],13.5],
	[[66.0,5.0,35.0,31.0,35.0,23.0,15.0,29.0,21.0],28.888889],
	[[95.0,76.0],85.5],
	[[34.0,5.0,62.0,27.0,29.0,33.0,6.0,23.0],27.375],
	[[19.0,29.0,13.0,23.0,22.0],21.2],
	[[34.0],34.0],
	[[17.0,38.0],27.5],
	[[40.0,14.0,6.0,23.0,28.0,13.0,13.0],19.57143],
	[[20.0,38.0,5.0,32.0,11.0,13.0,28.0],21],
	[[23.0,29.0,14.0,6.0],18],
	[[19.0,25.0,11.0,32.0,29.0,35.0,27.0,22.0],25],
	[[31.0,24.0,31.0,6.0,38.0,32.0,32.0],27.71429],
	[[35.0,50.0,39.0,28.0,15.0,31.0,39.0],33.85714],
	[[18.0],18.0],
	[[20.0],20.0],
	[[29.0,11.0,33.0],24.333333],
	[[17.0,15.0,39.0,33.0,7.0,26.0,14.0],21.57143],
	[[31.0,10.0,11.0],17.333333]
]

def set_message(id, target, operation, data_input = None):
	return message_helper.build_message_request_json(id, target, operation, data_input)

def set_read_message(sensor_name, test_identifier):
	global TEST_ITERATION
	id = 'TR-' + test_identifier + strftime('%Y%m%d%H%M%S') + '-' + str(TEST_ITERATION)
	return id, set_message(id, sensor_name, 'read')

def set_flush_message(sensor_name, test_identifier):
	global TEST_ITERATION
	id = 'TF-' + test_identifier + strftime('%Y%m%d%H%M%S') + '-' + str(TEST_ITERATION)
	return id, set_message(id, sensor_name, 'flush')

def set_compute_message(sensor_name, test_identifier, data_input = None):
	global TEST_ITERATION
	id = 'TC-' + test_identifier + strftime('%Y%m%d%H%M%S') + '-' + str(TEST_ITERATION)
	return id, set_message(id, sensor_name, 'compute', data_input) 

def on_request_received(status, msg, packet):

	global EXISTING_TESTS

	response = message_helper.decode_message(packet['payload'])
	id = response['id']

	EXISTING_TESTS[id].set_response(response)
	if EXISTING_TESTS[id].evaluate():
		print("Test " + id + " approved!")
	else:
		print("Test " + id + " rejected on criteria " + EXISTING_TESTS[id].get_first_criteria_to_fail().get_name() + "!")

### Testing methods

def read_single_value_from_temperature_sensor():

	global EXISTING_TESTS
	sensor_name = 'temperature_sensor'
	test_identifier = 'RSVFTS'

	id, request = set_read_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_float', lambda response : type(response['result']) is float)
	EXISTING_TESTS[id].add_criteria('value_within_range', lambda response : response['result'] >= specs[sensor_name]['expected_min_value'] and response['result'] <= specs[sensor_name]['expected_max_value'])
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])

	return id, request

def read_single_value_from_humidity_sensor():

	global EXISTING_TESTS
	sensor_name = 'humidity_sensor'
	test_identifier = 'RSVFHS'

	id, request = set_read_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_float', lambda response : type(response['result']) is float)
	EXISTING_TESTS[id].add_criteria('value_within_range', lambda response : response['result'] >= specs[sensor_name]['expected_min_value'] and response['result'] <= specs[sensor_name]['expected_max_value'])
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])

	return id, request

def flush_values_from_temperature_sensor():

	global EXISTING_TESTS
	sensor_name = 'temperature_sensor'
	test_identifier = 'FVFTS'

	id, request = set_flush_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_list', lambda response : type(response['result']) is list)
	EXISTING_TESTS[id].add_criteria('maximum_expected_length', lambda response : len(response['result']) <= 10)
	EXISTING_TESTS[id].add_criteria('values_within_range', lambda response : len(filter(lambda x: x < specs[sensor_name]['expected_min_value'] or x > specs[sensor_name]['expected_max_value'], response['result'])) == 0)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])
	
	return id, request

def flush_values_from_humidity_sensor():

	global EXISTING_TESTS
	sensor_name = 'humidity_sensor'
	test_identifier = 'FVFHS'

	id, request = set_flush_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_list', lambda response : type(response['result']) is list)
	EXISTING_TESTS[id].add_criteria('maximum_expected_length', lambda response : len(response['result']) <= 10)
	EXISTING_TESTS[id].add_criteria('values_within_range', lambda response : len(filter(lambda x: x < specs[sensor_name]['expected_min_value'] or x > specs[sensor_name]['expected_max_value'], response['result'])) == 0)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])

	return id, request

def compute_with_no_inputs_from_temperature_sensor():

	global EXISTING_TESTS
	sensor_name = 'temperature_sensor'
	test_identifier = 'CWNIFTS'

	id, request = set_compute_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_list', lambda response : type(response['result']) is list)
	EXISTING_TESTS[id].add_criteria('expected_length', lambda response : len(response['result']) == 3)
	EXISTING_TESTS[id].add_criteria('first_value_within_range', lambda response : response['result'][0] >= specs[sensor_name]['expected_min_value'] or response['result'][0] <= specs[sensor_name]['expected_max_value'])
	EXISTING_TESTS[id].add_criteria('second_value_equals_to_expected', lambda response : abs(response['result'][1] - (response['result'][0] * 1.8 + 32.0)) <= 1e-6)
	EXISTING_TESTS[id].add_criteria('third_value_equals_to_expected', lambda response : abs(response['result'][2] - (response['result'][0] + 273.15)) <= 1e-6)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])
	
	return id, request

def compute_with_no_inputs_from_humidity_sensor():

	global EXISTING_TESTS
	sensor_name = 'humidity_sensor'
	test_identifier = 'CWNIFHS'

	id, request = set_compute_message(sensor_name, test_identifier)

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_list', lambda response : type(response['result']) is list)
	EXISTING_TESTS[id].add_criteria('expected_length', lambda response : len(response['result']) == 2)
	EXISTING_TESTS[id].add_criteria('first_value_type_list', lambda response : type(response['result'][0]) is list)
	EXISTING_TESTS[id].add_criteria('second_value_none_if_list_empty', lambda response : len(response['result'][0]) > 0 or response['result'][1] == None)
	EXISTING_TESTS[id].add_criteria('first_values_within_range', lambda response : len(filter(lambda x: x < specs[sensor_name]['expected_min_value'] or x > specs[sensor_name]['expected_max_value'], response['result'][0])) == 0)
	EXISTING_TESTS[id].add_criteria('second_value_equals_to_average', lambda response : response['result'][1] == None or abs(response['result'][1] - (sum(response['result'][0]) / len(response['result'][0]))) <= 1e-6)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])
	
	return id, request

def compute_with_inputs_from_temperature_sensor():

	global EXISTING_TESTS
	global TEST_ORACLE_TEMPERATURE
	sensor_name = 'temperature_sensor'
	test_identifier = 'CWIFTS'

	index = random.randint(0, len(TEST_ORACLE_TEMPERATURE) - 1)
	id, request = set_compute_message(sensor_name, test_identifier, TEST_ORACLE_TEMPERATURE[index][0])

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_list', lambda response : type(response['result']) is list)
	EXISTING_TESTS[id].add_criteria('expected_length', lambda response : len(response['result']) == 2)
	EXISTING_TESTS[id].add_criteria('first_value_equals_to_expected', lambda response : abs(response['result'][0] - TEST_ORACLE_TEMPERATURE[index][1]) <= 1e-6)
	EXISTING_TESTS[id].add_criteria('second_value_equals_to_expected', lambda response : abs(response['result'][1] - TEST_ORACLE_TEMPERATURE[index][2]) <= 1e-6)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])
	
	return id, request

def compute_with_inputs_from_humidity_sensor():

	global EXISTING_TESTS
	global TEST_ORACLE_HUMIDITY
	sensor_name = 'humidity_sensor'
	test_identifier = 'CWIFHS'

	index = random.randint(0, len(TEST_ORACLE_HUMIDITY) - 1)
	id, request = set_compute_message(sensor_name, test_identifier, TEST_ORACLE_HUMIDITY[index][0])

	EXISTING_TESTS[id] = TestReport(request)
	EXISTING_TESTS[id].add_criteria('return_type_numerical', lambda response : type(response['result']) is float or type(response['result'] is int))
	EXISTING_TESTS[id].add_criteria('value_none_if_list_empty', lambda response : len(TEST_ORACLE_HUMIDITY[index][0]) > 0 or response['result'] == None)
	EXISTING_TESTS[id].add_criteria('value_equals_to_average', lambda response : (response['result'] == None and TEST_ORACLE_HUMIDITY[index][1] == None) or abs(response['result'] - TEST_ORACLE_HUMIDITY[index][1]) <= 1e-4)
	EXISTING_TESTS[id].add_criteria('maximum_elapsed_time_seconds', lambda response : response['timestamp'] - request['timestamp'] <= specs[sensor_name]['readings_delay_ms'])
	
	return id, request

#TESTING_METHODS = [read_single_value_from_temperature_sensor, read_single_value_from_humidity_sensor, flush_values_from_temperature_sensor, flush_values_from_humidity_sensor]
#TESTING_METHODS = [compute_with_no_inputs_from_temperature_sensor, compute_with_no_inputs_from_humidity_sensor]

TESTING_METHODS = [compute_with_inputs_from_temperature_sensor, compute_with_inputs_from_humidity_sensor]

def main():

	global TESTING_METHODS
	global EXISTING_TESTS
	global TEST_ITERATION
	global MAX_ITERATIONS

	mqtt_adapter.setup('TEST_AGENT')
	mqtt_adapter.setOnMessageReceived(on_request_received)
	random.seed(time())

	while True:

		if TEST_ITERATION <= MAX_ITERATIONS:
			
			TEST_ITERATION += 1
			print("Starting test iteration " + str(TEST_ITERATION) + "...")

			for test_method in TESTING_METHODS:
				
				execute_test = random.randint(0, 1)
				if execute_test <= 1:
					id, request = test_method()
					mqtt_adapter.publish_to_requests(message_helper.encode_message(request))

		elif pending_tests == 0:
				break

		pending_tests = len(filter(lambda x : x.is_in_progress(), EXISTING_TESTS.values()))
		approved_tests = len(filter(lambda x : x.is_accepted(), EXISTING_TESTS.values()))
		total_tests = len(EXISTING_TESTS)

		print("Pending tests: " + str(pending_tests) + ". Accepted tests: " + str(approved_tests) + "/" + str(total_tests))
		if int(TEST_ITERATION) % 5 == 0:
			sleep(8.0)
		else:
			sleep(random.uniform(1.0, 2.0))

if __name__ == "__main__":
	main()