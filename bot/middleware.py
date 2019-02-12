import json
import os

import falcon

VK_GROUP_ID = os.environ.get('GROUP_ID')


class JSONMiddleware(object):
    def process_request(self, req, resp):
        if not req.content_length:
            raise falcon.HTTPBadRequest('Not empty')

        try:
            req.context['data'] = json.loads(req.stream.read())
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPBadRequest('Not valid JSON')


class SecretKeyMiddleware(object):
    def process_request(self, req, resp):
        data = req.context['data']
        if os.environ.get('SECRET_KEY') != data.get('secret'):
            raise falcon.HTTPBadRequest('Invalid SECRET_KEY')


class CheckGroupMiddleware(object):
    def process_request(self, req, resp):
        data = req.context['data']
        if int(VK_GROUP_ID) != data.get('group_id'):
            raise falcon.HTTPBadRequest('GROUP_ID is required')

