import io
from urllib.parse import urlsplit, urljoin

import requests
import vk

from .error import InstagramError
from .config import GROUP_ID, GROUP_TOKEN

api = vk.Api(GROUP_TOKEN)
group = api.get_group(GROUP_ID)


class Bot(object):
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        group.messages_set_typing()

        if "message_new" == data.get("type"):
            message_object = data['object']
            message_text = message_object['body']
            user_id = message_object['user_id']

            if not self.is_instagram_link(message_text):
                group.send_messages(message_object['user_id'], message='Отправьте пожалуйста ссылку на фото из instagram.com')
            else:
                try:
                    instagram_photo = self.get_instagram_photo(instagram_photo_link=message_text)
                    group.send_messages(message_object['user_id'], image_files=[instagram_photo])
                except InstagramError:
                    group.send_messages(message_object['user_id'], message='Не могу найти фото, проверьте пожалуйста ссылку')

            user = api.get_user(user_id)
            if user not in group:
                group.send_messages(message_object['user_id'], message='Пожалуйста не забудьте подписать на https://vk.com/instasave_bot :v:')

    def is_instagram_link(self, link):
        url = urlsplit(link)
        if url.netloc in ["www.instagram.com", "instagram.com"]:
            return True

        return False

    def get_instagram_photo(self, instagram_photo_link):
        if not instagram_photo_link.endswith('/'):
            instagram_photo_link += '/'

        url = urljoin(instagram_photo_link, 'media/?size=l')
        response = requests.get(url)
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        return file_like
