from rest_api.rest_api import app

from mongomock import MongoClient
from unittest import TestCase
from unittest.mock import patch
import json


class TestRestApi(TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000/api'
        self.db = MongoClient().db
        self.patcher = patch('rest_api.rest_api.db', self.db)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_post_bad_request_invalid_data(self):
        app_test = app.test_client(self)
        r = app_test.post('/api', data=dict(teste='teste'))
        self.assertEqual(400, r.status_code)

    def test_post_bad_request_no_json(self):
        app_test = app.test_client(self)
        r = app_test.post('/api', data='teste')
        self.assertEqual(400, r.status_code)

    def test_post_valid_json_invalid_parameters(self):
        app_test = app.test_client(self)
        r = app_test.post('/api', data=json.dumps({"message": {"teste": "teste"}}), content_type='application/json')
        self.assertEqual(400, r.status_code)

    def test_post_valid_json_valid_parameters(self):
        app_test = app.test_client(self)
        valid_json = {
            'message': {
                'user': 'sample_user',
                'room': 'sample_room',
                'date_time': 'sample_date_time',
                'message': 'sample_message'
            }
        }
        r = app_test.post('/api', data=json.dumps(valid_json), content_type='application/json')
        self.assertEqual(201, r.status_code)

    def test_post_valid_json_valid_parameters_and_get_room_data(self):
        app_test = app.test_client(self)
        valid_json = {
            'message': {
                'user': 'sample_user',
                'room': 'sample_room',
                'date_time': 'sample_date_time',
                'message': 'sample_message'
            }
        }
        r = app_test.post('/api', data=json.dumps(valid_json), content_type='application/json')
        self.assertEqual(201, r.status_code)

        rg = app_test.get('api/sample_room')
        self.assertEqual(200, rg.status_code)

        data = json.loads(rg.get_data(as_text=True))
        self.assertEqual(1, len(data['history']))

    def test_post_valid_json_valid_parameters_and_get_correct_room_data(self):
        app_test = app.test_client(self)
        valid_json = {
            'message': {
                'user': 'sample_user',
                'room': 'sample_room',
                'date_time': 'sample_date_time',
                'message': 'sample_message'
            }
        }
        for i in range(3):
            r = app_test.post('/api', data=json.dumps(valid_json), content_type='application/json')
            self.assertEqual(201, r.status_code)

        valid_json['message']['room'] = 'second_room'
        for i in range(5):
            r = app_test.post('/api', data=json.dumps(valid_json), content_type='application/json')
            self.assertEqual(201, r.status_code)

        rg = app_test.get('api/sample_room')
        self.assertEqual(200, rg.status_code)

        data = json.loads(rg.get_data(as_text=True))
        self.assertEqual(3, len(data['history']))

        rg = app_test.get('api/second_room')
        self.assertEqual(200, rg.status_code)

        data = json.loads(rg.get_data(as_text=True))
        self.assertEqual(5, len(data['history']))
