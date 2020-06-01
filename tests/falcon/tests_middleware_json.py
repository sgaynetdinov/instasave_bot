import os

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware


class JSONMiddlewareTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = falcon.API(middleware=[JSONMiddleware()])
        self.app.add_route('/', testing.SimpleTestResource(json={'title': 'Success test'}))

    def test_empty_request(self):
       got = self.simulate_post('/')

       self.assertEqual(got.json['title'], 'Not empty')
       self.assertEqual(got.status, falcon.HTTP_400)

    def test_not_valid_json(self):
       got = self.simulate_post('/', body=b'{a: 3}')

       self.assertEqual(got.json['title'], 'Not valid JSON')
       self.assertEqual(got.status, falcon.HTTP_400)

    def test_valid_json(self):
        got = self.simulate_post('/', body=b'{"a": 1}')

        self.assertEqual(got.json['title'], 'Success test')
        self.assertEqual(got.status, falcon.HTTP_200)
