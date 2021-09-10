import os
from multiprocessing import Process
from urllib.request import urlopen

import vk

from .instagram import Instagram, Instagram404Error, InstagramLinkError

VK_GROUP_TOKEN = os.environ.get('GROUP_TOKEN')
VK_GROUP_ID = os.environ.get('GROUP_ID')
MESSAGE_IF_NOT_MEMBERS = os.environ.get("MESSAGE_IF_NOT_MEMBERS")

api = vk.Api(VK_GROUP_TOKEN)
group = api.get_group(VK_GROUP_ID)


class Bot:
    def on_post(self, req, resp):
        data = req.context['data']

        if data.get("type") == "confirmation":
            resp.data = bytes(os.environ.get('CONFIRMATION_KEY'), 'ascii')
        else:
            resp.data = b'ok'

        if data.get("type") == "message_new":
            link = data['object']['text']
            user_id = data['object']['from_id']
            Process(target=self.handler_new_message, args=(link, user_id,)).start()

    def handler_new_message(self, link, user_id):
        group.messages_set_typing(user_id)

        try:
            instagram = Instagram.from_url(link)
        except Instagram404Error:
            group.send_messages(user_id, message='Не могу найти, возможно фото/видео доступно только для подписчиков (приватный аккаунт)')
        except InstagramLinkError:
            group.send_messages(user_id, message='Отправьте пожалуйста ссылку на фото из Instagram')
        else:
            user_is_member = user_id in group
            self.send_message(instagram, user_id, user_is_member)

    def send_message(self, instagram, user_id, user_is_member):
        text = instagram.get_text()
        if text:
            group.send_messages(user_id, message=text)

        urls = instagram.get_photos_and_video_url()
        if not user_is_member and MESSAGE_IF_NOT_MEMBERS:
            urls = urls[:1]

        for url in urls:
            group.messages_set_typing(user_id)
            if '.mp4' in url:
                group.send_messages(user_id, message=url)
            else:
                group.send_messages(user_id, image_files=[urlopen(url)])
            if not user_is_member and MESSAGE_IF_NOT_MEMBERS:
                group.messages_set_typing(user_id)
                group.send_messages(user_id, message=MESSAGE_IF_NOT_MEMBERS)

