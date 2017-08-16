import io
import json
import os
from urllib.parse import urlsplit, urljoin

import falcon
import requests
import vk

SECRET_KEY = os.environ.get('SECRET_KEY')
GROUP_ID = int(os.environ.get('GROUP_ID'))
GROUP_TOKEN = os.environ.get('GROUP_TOKEN')
CONFIRMATION_KEY = os.environ.get('CONFIRMATION_KEY')

api = vk.Api(GROUP_TOKEN)
group = api.get_group(GROUP_ID)


class InstagramError(Exception):
    pass


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


class Bot(object):
    def on_post(self, req, resp):
        data = req.context['data']

        if "message_new" == data.get("type"):
            message_object = data['object']
            message_text = message_object['body']

            if not self.is_instagram_link(message_text):
                group.send_messages(message_object['user_id'], message='Отправьте пожалуйста ссылку на фото из instagram.com')
            else:
                try:
                    instagram_photo = self.get_instagram_photo(instagram_photo_link=message_text)
                    group.send_messages(message_object['user_id'], image_files=[instagram_photo])
                except InstagramError:
                    group.send_messages(message_object['user_id'], message='Не могу найти фото, проверьте пожалуйста ссылку')

        resp.data = b'ok'

    def is_instagram_link(self, link):
        url = urlsplit(link)
        if url.netloc in ["www.instagram.com", "instagram.com"]:
            return True

        return False

    def get_instagram_photo(self, instagram_photo_link):
        url = urljoin(instagram_photo_link, 'media/?size=l')
        response = requests.get(url)
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        return file_like


application = start = falcon.API(middleware=[
    JSONMiddleware(),
    SecretKeyMiddleware(),
    CheckGroupMiddleware(),
    ConfirmationMiddleware()
])

application.add_route('/', Bot())
