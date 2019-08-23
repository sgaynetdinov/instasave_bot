import os
from unittest.mock import patch

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware
from bot.vk_bot import Process
from bot.wsgi import application

os.environ['CONFIRMATION_KEY'] = 'response confirmation'
os.environ['GROUP_ID'] = '100500'
os.environ['SECRET_KEY'] = 'SECRET'


class ConfirmationTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = application

    @patch('bot.vk_bot.Process.start')
    def test_type_message_new(self, mock):
        got = self.simulate_post('/', body=b'{"type": "message_new", "object": {"body": 100500, "user_id": 200600}, "secret": "SECRET", "group_id": 100500}')

        self.assertEqual(mock.call_count, 1)

    def test_type_not_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "message_reply", "group_id": 100500, "secret": "SECRET"}')

        self.assertEqual(got.text, 'ok')

    def test_type_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "confirmation", "group_id": 100500, "secret": "SECRET"}')

        self.assertEqual(got.text, 'response confirmation')
