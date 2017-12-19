import json

import falcon

import opbeat.instrumentation.control
from opbeat.utils import build_name_with_http_method_prefix

from .config import VK_SECRET_KEY, VK_GROUP_ID, VK_CONFIRMATION_KEY

opbeat.instrumentation.control.instrument()


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
        if VK_SECRET_KEY != data.get('secret') and "confirmation" != data.get('type'):
            raise falcon.HTTPBadRequest('Invalid request')


class CheckGroupMiddleware(object):
    def process_request(self, req, resp):
        data = req.context['data']
        if VK_GROUP_ID != data.get('group_id'):
            raise falcon.HTTPBadRequest('Invalid request')


class ConfirmationMiddleware(object):
    def process_response(self, req, resp, resource):
        data = req.context['data']
        if "confirmation" == data.get("type"):
            resp.data = bytes(VK_CONFIRMATION_KEY, 'ascii')


class OpbeatAPMMiddleware(object):
    """
    https://gist.github.com/matagus/ecec9db26db2143e196f659161bc5918
    """

    def __init__(self, client):
        self.client = client

    def process_request(self, req, resp):
        self.client.begin_transaction("web.falcon")

    def process_response(self, req, resp, resource):
        name = "{}.{}".format(
            resource.__class__.__module__,
            resource.__class__.__name__
        )

        rule = build_name_with_http_method_prefix(name, req)

        try:
            status_code = int(resp.status.split(" ")[0])
        except (IndexError, TypeError):
            status_code = 200

        self.client.end_transaction(rule, status_code)
