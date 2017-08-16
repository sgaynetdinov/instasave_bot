import io
import os
from urllib.parse import urlsplit, urljoin

import requests
import vk
from botanio import botan

from .error import InstagramError

GROUP_ID = int(os.environ.get('GROUP_ID'))
GROUP_TOKEN = os.environ.get('GROUP_TOKEN')
BOTAN_TOKEN = os.environ.get('BOTAN_TOKEN')

api = vk.Api(GROUP_TOKEN)
group = api.get_group(GROUP_ID)


class Bot(object):
    def on_post(self, req, resp):
        data = req.context['data']

        if "message_new" == data.get("type"):
            message_object = data['object']
            message_text = message_object['body']

            if not self.is_instagram_link(message_text):
                group.send_messages(message_object['user_id'], message='Отправьте пожалуйста ссылку на фото из instagram.com')
                botan.track(BOTAN_TOKEN, message_object['user_id'], message_text, "is_not_link_instagram")
            else:
                try:
                    instagram_photo = self.get_instagram_photo(instagram_photo_link=message_text)
                    group.send_messages(message_object['user_id'], image_files=[instagram_photo])
                    botan.track(BOTAN_TOKEN, message_object['user_id'], message_text, "send_instagram_photo")
                except InstagramError:
                    group.send_messages(message_object['user_id'], message='Не могу найти фото, проверьте пожалуйста ссылку')
                    botan.track(BOTAN_TOKEN, message_object['user_id'], message_text, "not_found_instagram_link")

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
