import json
import unittest
import os

from app_setup import create_app


class TestMovingAverageWeekly(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["FLASK_ENV"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client(use_cookies=True)
        self.base_url = '/sensors/moving-average-weekly?'

    def test_when_not_any_query_params_given_returns_400(self):
        url = self.base_url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_when_sensor_id_not_in_query_params_returns_400(self):
        url = self.base_url + 'date=12/9/2020'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_when_date_not_in_query_params_returns_400(self):
        url = self.base_url + 'sensor-id=PFJ40'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 400)

    def test_when_date_not_in_valid_format_returns_400(self):
        url = self.base_url + 'sensor-id=PFJ40&date=11-09-2020'
        resp = self.client.get(url)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'dateParsingError')

    def test_when_week_1_not_have_any_sensor_values_returns_404(self):
        url = self.base_url + 'sensor-id=PFJ40&date=01/01/2020'
        resp = self.client.get(url)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['error_type'], 'sensorValuesError')

    def test_when_week_2_not_have_any_sensor_values_returns_404(self):
        url = self.base_url + 'sensor-id=PFJ40&date=30/09/2020'
        resp = self.client.get(url)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['error_type'], 'sensorValuesError')

    def test_when_moving_average_diff_correct_returns_200(self):
        url = self.base_url + 'sensor-id=PFJ40&date=03/9/2020'
        resp = self.client.get(url)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['difference'], -0.44401653439153255)