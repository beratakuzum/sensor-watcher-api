import fastjsonschema

from flask import Blueprint, jsonify
from flask import request

from src.utils.dates import check_date_valid_format
from src.utils.errors import API_ERROR
from src.utils.validators import check_required_query_params_exist, validate_body
from src.services.sensors import get_moving_average_diff_two_weeks, get_moving_average_diff_two_periods

# we define json-schema to validate request body of '/moving-average-period' endpoint
SENSOR_VALUES_PERIODS_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'date start-Period 1': {'type': 'string'},
        'date end-Period 1': {'type': 'string'},
        'date start-Period 2': {'type': 'string'},
        'date end-Period 2': {'type': 'string'},
        'sensor-id': {'type': 'string'}
    },
    'required': ['date start-Period 1', 'date end-Period 1', 'date start-Period 2',
                 'date end-Period 2', 'sensor-id']
}
SENSOR_VALUES_PERIODS_SCHEMA_VALIDATOR = fastjsonschema.compile(SENSOR_VALUES_PERIODS_SCHEMA)

sensors_bp = Blueprint('sensors', __name__)


# endpoint to calculate difference between moving average of "i week" and "i+1" week
@sensors_bp.route('/moving-average-weekly', methods=['GET'])
@check_required_query_params_exist(['sensor-id', 'date'])
def calculate_moving_average_weekly():
    sensor_id = request.args.get('sensor-id')
    date = request.args.get('date')

    # Checking if the input date is in the %d/%m/%Y format
    date_format = "%d/%m/%Y"
    date_object = check_date_valid_format(input_date=date, date_format=date_format)
    if not date_object:
        raise API_ERROR(
            error_type="dateParsingError",
            message=f"<date> parameter must be a valid date in '{date_format}' format",
            status_code=400
        )

    result = get_moving_average_diff_two_weeks(sensor_id=sensor_id, input_date_object=date_object)

    return jsonify(result)


# endpoint to calculate difference between moving average of two given periods
@sensors_bp.route('/moving-average-period', methods=['POST'])
def calculate_moving_average_for_two_periods():
    request_body = request.json
    validate_body(request_body, SENSOR_VALUES_PERIODS_SCHEMA_VALIDATOR)

    periods = dict()

    # Checking if the input dates are in the %d/%m/%Y format and get the datetime objects if valid
    date_format = "%d/%m/%Y %H:%M"
    periods["period_1_start"] = check_date_valid_format(request_body['date start-Period 1'], date_format)
    periods["period_1_end"] = check_date_valid_format(request_body['date end-Period 1'], date_format)
    periods["period_2_start"] = check_date_valid_format(request_body['date start-Period 2'], date_format)
    periods["period_2_end"] = check_date_valid_format(request_body['date end-Period 2'], date_format)

    for period_name, date in periods.items():
        if not date:
            raise API_ERROR(
                error_type="dateParsingError",
                message=f"<{period_name}> must be a valid date in '{date_format}' format",
                status_code=400
            )

    if periods["period_1_end"] <= periods["period_1_start"]:
        raise API_ERROR(
            error_type="periodError",
            message=f"date end-Period 1 must be newer than date start-Period 1",
            status_code=400
        )

    if periods["period_2_end"] <= periods["period_2_start"]:
        raise API_ERROR(
            error_type="periodError",
            message=f"date end-Period 2 must be newer than date start-Period 2",
            status_code=400
        )

    sensor_id = request_body['sensor-id']

    result = get_moving_average_diff_two_periods(periods=periods, sensor_id=sensor_id)

    return jsonify(result)
