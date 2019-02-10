import os

os.environ['CONFIRMATION_KEY'] = 'response confirmation'

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware, ConfirmationMiddleware


class ConfirmationMiddlewareTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = falcon.API(middleware=[JSONMiddleware(), ConfirmationMiddleware()])
        self.app.add_route('/', testing.SimpleTestResource())

    def test_type_not_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "message_new"}')

        self.assertEqual(got.text, '')

    def test_type_confirmation(self):
        got = self.simulate_post('/', body=b'{"type": "confirmation"}')

        self.assertEqual(got.text, 'response confirmation')

