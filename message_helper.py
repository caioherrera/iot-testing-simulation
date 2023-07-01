import json
from time import *

'''
request_message_expected = {
    'id': 'U20230625140400',
    'timestamp': '2023-06-25 14:04:00 GMT-3'
    'target': 'temperature_sensor'
    'operation': 'read/flush'
}

read_response_message_expected = {
    'id': 'U20230625140400',
    'timestamp': '2023-06-25 14:04:05 GMT-3'
    'result': '23.099999'
}

flush_response_message_expected = {
    'id': 'U20230625140400',
    'timestamp': '2023-06-25 14:04:05 GMT-3'
    'result': ['23.099999', '15.0999999'....]
}
'''

def decode_message(payload):
    return json.loads(payload)

def encode_message(message):
    return json.dumps(message)

def build_message_request_json(id, target, operation, data_input = None):
    message = {
        'id': id,
        'timestamp': time(),
        'target': target,
        'operation': operation
    }
    if data_input != None:
        message['data_input'] = data_input
    return message

def build_message_response_json(id, result):
    message = {
        'id': id,
        'timestamp': time(),
        'result': result
    }
    return message

def build_message_request(id, target, operation):
    return encode_message(build_message_request_json(id, target, operation))

def build_message_response(id, result):
    return encode_message(build_message_response_json(id, result))