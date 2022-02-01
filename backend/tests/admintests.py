import unittest
from backend import admin
import json
from unittest.mock import patch

import requests

URL_BACK = 'http://192.168.10.2:5001'


class TestAdminCanRemove(unittest.TestCase):
    def setUp(self):
        self.user_id = 1

    @patch('requests.post')
    def test_remove_user(self, mock_post):
        info = {"id": 3}
        resp = requests.post(URL_BACK + "/remove", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        print(resp)
        mock_post.assert_called_with(URL_BACK + "/remove", data=json.dumps(info),
                                     headers={'Content-Type': 'application/json'})
