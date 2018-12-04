import io
from multiprocessing import Process

import requests
import vk

from .config import VK_GROUP_ID, VK_GROUP_TOKEN
from .instagram import Instagram, Instagram404Error

api = vk.Api(VK_GROUP_TOKEN)
group = api.get_group(VK_GROUP_ID)


class Bot:
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        if "message_new" == data.get("type"):
            Process(target=handler_new_message, args=(data,)).start()


def handler_new_message(data):
    message_text = data['object']['body']
    user_id = data['object']['user_id']

    user = api.get_user(user_id)

    if not Instagram.is_instagram_link(message_text):
        group.send_messages(user.id, message='Отправьте пожалуйста ссылку на фото из Instagram')
        return None

    send_message(message_text, user)


def send_message(instagram_link, user):
    group.messages_set_typing(user)

    try:
        instagram = Instagram.from_url(instagram_link)
    except Instagram404Error:
        group.send_messages(user.id, message='Не могу найти, возможно фото/видео доступно только для подписчиков (приватный аккаунт)')
        return

    group.send_messages(user.id, message=instagram.get_text())

    photo_urls = instagram.get_photos_url()
    for instagram_photo in get_photos(photo_urls):
        group.messages_set_typing(user)
        group.send_messages(user.id, image_files=[instagram_photo])


def get_photos(urls):
    for url in urls:
        response = requests.get(url)
        file_like = ('photo.jpg', io.BytesIO(response.content))
        yield file_like
