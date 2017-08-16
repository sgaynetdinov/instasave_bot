import json
import os

import falcon

SECRET_KEY = os.environ.get('SECRET_KEY')
GROUP_ID = int(os.environ.get('GROUP_ID'))
CONFIRMATION_KEY = os.environ.get('CONFIRMATION_KEY')


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
        if SECRET_KEY != data.get('secret') and "confirmation" != data.get('type'):
            raise falcon.HTTPBadRequest('Invalid request')


class CheckGroupMiddleware(object):
    def process_request(self, req, resp):
        data = req.context['data']
        if GROUP_ID != data.get('group_id'):
            raise falcon.HTTPBadRequest('Invalid request')


class ConfirmationMiddleware(object):
    def process_response(self, req, resp, resource):
        data = req.context['data']
        if "confirmation" == data.get("type"):
            resp.data = bytes(CONFIRMATION_KEY, 'ascii')
