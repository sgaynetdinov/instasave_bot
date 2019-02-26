import os

import falcon
from falcon import testing

from bot.middleware import CheckGroupMiddleware, JSONMiddleware

os.environ['GROUP_ID'] = '100500'


class CheckGroupMiddlewareTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = falcon.API(middleware=[JSONMiddleware(), CheckGroupMiddleware()])
        self.app.add_route('/', testing.SimpleTestResource(body='success response'))

    def test_with_group_id(self):
        got = self.simulate_post('/', body=b'{"group_id": 100500}')

        self.assertEqual(got.status, falcon.HTTP_200)
        self.assertEqual(got.text, 'success response')

    def test_without_group_id(self):
        got = self.simulate_post('/', body=b'{"type": "message_new"}')

        self.assertEqual(got.status, falcon.HTTP_400)
        self.assertEqual(got.json['title'], 'GROUP_ID is required')
