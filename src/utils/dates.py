from src.utils.errors import API_ERROR
from datetime import datetime, timedelta


def check_date_valid_format(input_date, date_format):
    """Checking if the input date is in the format specified by date_format parameter and returning the datetime
    object if valid"""
    try:
        date_object = datetime.strptime(input_date, date_format)
    except Exception as e:
        return

    return date_object


def get_week_period(date_object):
    """Finds the start and end of the week the date_object is in"""
    start = date_object - timedelta(days=date_object.weekday())
    end = start + timedelta(days=7)
    return start, end


def check_period_intervals_valid(periods):

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
