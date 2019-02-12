import os

os.environ['CONFIRMATION_KEY'] = 'response confirmation'
os.environ['GROUP_ID'] = '100500'
os.environ['SECRET_KEY'] = 'SECRET'

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware
from bot.wsgi import application


class ConfirmationTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = application

    def test_type_not_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "message_reply", "group_id": 100500, "secret": "SECRET"}')

        self.assertEqual(got.text, 'ok')

    def test_type_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "confirmation", "group_id": 100500, "secret": "SECRET"}')

        self.assertEqual(got.text, 'response confirmation')

