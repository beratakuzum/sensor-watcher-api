import unittest

from src.utils.dates import check_date_valid_format, get_week_period
from src.utils.errors import API_ERROR

from datetime import datetime


class TestDateUtils(unittest.TestCase):
    def test_check_invalid_date_format_returns_None(self):
        date = '12/9/2020'
        date_object = check_date_valid_format(input_date=date, date_format='%d/%m/%Y')
        self.assertTrue(isinstance(date_object, datetime))

        date = '2020/12/1'
        date_object = check_date_valid_format(input_date=date, date_format='%d/%m/%Y')
        self.assertTrue(date_object is None)

        date = '12-9-2020'
        date_object = check_date_valid_format(input_date=date, date_format='%d-%m-%Y')
        self.assertTrue(isinstance(date_object, datetime))

    def test_it_will_give_start_and_end_of_week_period(self):
        date_object = datetime.strptime('03/09/2020', '%d/%m/%Y')
        start, end = get_week_period(date_object=date_object)
        assert start == datetime.strptime('31/08/2020', '%d/%m/%Y')
        assert end == datetime.strptime('7/09/2020', '%d/%m/%Y')


class TestApiErrorHandler(unittest.TestCase):
    def test_when_details_not_given_api_error_has_no_details_field(self):
        api_error = API_ERROR(
            message="foo",
            status_code=0,
            error_type="bar"
        )
        to_dict = api_error.to_dict()

        assert 'details' not in to_dict

    def test_when_details_given_api_error_has_details_field(self):
        api_error = API_ERROR(
            message="foo",
            status_code=0,
            error_type="bar",
            details="foobar"
        )
        to_dict = api_error.to_dict()

        assert 'details' in to_dict
