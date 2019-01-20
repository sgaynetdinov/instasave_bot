import io
import os
from multiprocessing import Process
from urllib.request import urlopen

import vk

from .instagram import Instagram, Instagram404Error

VK_GROUP_ID = int(os.environ.get('GROUP_ID'))
VK_GROUP_TOKEN = os.environ.get('GROUP_TOKEN')

api = vk.Api(VK_GROUP_TOKEN)
group = api.get_group(VK_GROUP_ID)


class Bot:
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        if "message_new" == data.get("type"):
            Process(target=handler_new_message, args=(data,)).start()


def handler_new_message(data):
    link = data['object']['body']
    user_id = data['object']['user_id']

    group.messages_set_typing(user_id)

    if not Instagram.is_instagram_link(link):
        group.send_messages(user_id, message='Отправьте пожалуйста ссылку на фото из Instagram')
        return

    try:
        instagram = Instagram.from_url(link)
    except Instagram404Error:
        group.send_messages(user_id, message='Не могу найти, возможно фото/видео доступно только для подписчиков (приватный аккаунт)')
    else:
        group.send_messages(user_id, message=instagram.get_text())
        for url in instagram.get_photos_url():
            group.messages_set_typing(user_id)
            group.send_messages(user_id, image_files=[urlopen(url)])
