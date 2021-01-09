import json
import os
import unittest

from app_setup import create_app


class TestMovingAveragePeriod(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["FLASK_ENV"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client(use_cookies=True)
        self.base_url = '/sensors/moving-average-period?'

    def test_when_no_request_body_given_gets_400(self):
        url = self.base_url
        resp = self.client.post(url)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_no_period_1_start_given_returns_400(self):
        url = self.base_url
        req_body = {
            # "date start-Period 1": "11/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }

        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_no_period_1_end_given_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "11/09/2020 12:00",
            # "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }

        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_no_period_2_start_given_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "11/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            # "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }

        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_no_period_2_end_given_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "11/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            # "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }

        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_no_sensor_id_given_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "11/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            # "sensor-id": "FFM40"
        }

        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'requestBodyError')

    def test_when_period_1_end_smaller_than_or_equal_to_start_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "12/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'periodError')

        req_body['date start-Period 1'] = "13/09/2020 12:00"
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'periodError')

    def test_when_period_2_end_smaller_than_or_equal_to_start_returns_400(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "10/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "22/09/2020 13:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'periodError')

        req_body['date start-Period 2'] = "23/09/2020 13:00"
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['error_type'], 'periodError')

    def test_when_period_1_has_no_sensor_values_returns_404(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "10/10/2020 12:00",
            "date end-Period 1": "12/10/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['error_type'], 'sensorValuesError')

    def test_when_period_2_has_no_sensor_values_returns_404(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "10/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/10/2020 12:00",
            "date end-Period 2": "22/10/2020 13:00",
            "sensor-id": "FFM40"
        }
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(data['error_type'], 'sensorValuesError')

    def test_when_moving_average_period_correct_returns_200(self):
        url = self.base_url
        req_body = {
            "date start-Period 1": "11/09/2020 12:00",
            "date end-Period 1": "12/09/2020 12:00",
            "date start-Period 2": "20/09/2020 12:00",
            "date end-Period 2": "22/09/2020 13:00",
            "sensor-id": "FFM40"
        }
        resp = self.client.post(url, json=req_body)
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['difference'], -1.211802163007519)