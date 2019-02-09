import os

os.environ['GROUP_ID'] = '1'
        
from urllib.parse import urlencode

import falcon
from falcon import testing

from bot.middleware import JSONMiddleware, SecretKeyMiddleware, CheckGroupMiddleware, ConfirmationMiddleware


class FalconBaseTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()

        self.app = falcon.API(middleware=[
            JSONMiddleware(),
            SecretKeyMiddleware(),
            CheckGroupMiddleware(),
            ConfirmationMiddleware()
        ])
        self.app.add_route('/', testing.SimpleTestResource())

class JSONMiddlewareTestCase(FalconBaseTestCase):
    def test_empty_request(self):
       got = self.simulate_post('/') 

       self.assertEqual(got.json['title'], 'Not empty')
       self.assertEqual(got.status, falcon.HTTP_400)

    def test_not_valid_json(self):
       got = self.simulate_post('/', body=b'{a: 3}')
       
       self.assertEqual(got.json['title'], 'Not valid JSON')
       self.assertEqual(got.status, falcon.HTTP_400)

