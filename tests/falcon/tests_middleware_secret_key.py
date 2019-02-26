import os

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware, SecretKeyMiddleware

os.environ['SECRET_KEY'] = 'SECRET'


class SecretKeyMiddlewareTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = falcon.API(middleware=[JSONMiddleware(), SecretKeyMiddleware()])
        self.app.add_route('/', testing.SimpleTestResource(json={'title': 'Success test'}))

        self.data = b'{"secret": "SECRET", "type": "message_new"}'

    def test_valid_secret(self):
        got = self.simulate_post('/', body=self.data)

        self.assertEqual(got.json['title'], 'Success test')
        self.assertEqual(got.status, falcon.HTTP_200)

    def test_invalid_secret(self):
        got = self.simulate_post('/', body=b'{"secret": "INVALID_SECRET", "type": "message_new"}')

        self.assertEqual(got.json['title'], 'Invalid SECRET_KEY')
        self.assertEqual(got.status, falcon.HTTP_400)
