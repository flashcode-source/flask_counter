"""A Demo Counter App Using Flask"""

from flask import Flask
from app.statuscodes import STATUS_CODE_CREATED, STATUS_CODE_DUPLICATE, \
      STATUS_CODE_NOT_FOUND, STATUS_CODE_OK

app = Flask("Counter App")

COUNTERS = {}


@app.route('/counters/<name>', methods=['post'])
def create_counter(name):
    """Create a counter"""
    global COUNTERS
    if name not in COUNTERS:
        COUNTERS[name] = 0
        return {'data': COUNTERS, 'message': 'counter created', 'error': None},  STATUS_CODE_CREATED
    return {'data': None, 'message': f'cannot create counter {name}'}, \
        STATUS_CODE_DUPLICATE


@app.route('/counters/<name>', methods=['get'])
def get_counter(name):
    """get counter"""
    global COUNTERS
    if name in COUNTERS:
        return {'data': COUNTERS, 'message': f'counter {name} found'}, STATUS_CODE_OK
    return {'data': None, 'message': f'counter {name} not found'}, STATUS_CODE_NOT_FOUND


@app.route('/counters/<name>/increment', methods=['put'])
def increment_counter(name):
    """increment counter"""
    app.logger.debug(f'Requesting to increment counter {name}')
    COUNTERS[name] = COUNTERS[name] + 1
    app.logger.debug(f'counter {name} had been incremented')
    return {'data': COUNTERS, 'message': f'counter {name} incremented'}, STATUS_CODE_OK
