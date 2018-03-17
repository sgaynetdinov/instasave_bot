import threading

import vk

from .config import VK_GROUP_ID, VK_GROUP_TOKEN
from .instagram import is_instagram_link, get_instagram_photos, InstagramError

api = vk.Api(VK_GROUP_TOKEN)
group = api.get_group(VK_GROUP_ID)


def send_message(instagram_link, user):
    group.messages_set_typing(user)

    if not is_instagram_link(instagram_link):
        group.send_messages(user.id, message='Отправьте пожалуйста ссылку на фото из instagram.com')
        return None

    try:
        for instagram_photo in get_instagram_photos(instagram_link):
            group.send_messages(user.id, image_files=[instagram_photo])
            group.messages_set_typing(user)
    except InstagramError:
        group.send_messages(user.id, message='Не могу найти, возможно фото/видео доступно только для подписчиков (приватный аккаунт)')


class Bot(object):
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        if "message_new" == data.get("type"):
            message_object = data['object']
            message_text = message_object['body']
            user_id = message_object['user_id']

            user = api.get_user(user_id)

            if user not in group:
                group.messages_set_typing(user)
                group.send_messages(message_object['user_id'], message='Пожалуйста вступите в сообщество https://vk.com/instasave_bot :v:')

            threading.Thread(target=send_message, args=(message_text, user)).start()
