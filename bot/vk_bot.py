import vk

from .config import VK_GROUP_ID, VK_GROUP_TOKEN
from .instagram import is_instagram_link, get_instagram_photos, InstagramError

api = vk.Api(VK_GROUP_TOKEN)
group = api.get_group(VK_GROUP_ID)


class Bot:
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        if "message_new" == data.get("type"):
            self.handler_new_message(data)

    def handler_new_message(self, data):
        message_text = data['object']['body']
        user_id = data['object']['user_id']

        user = api.get_user(user_id)

        if user not in group:
            group.messages_set_typing(user)
            group.send_messages(user_id, message='Пожалуйста вступите в сообщество https://vk.com/instasave_bot :v:')

        self.send_message(message_text, user)

    def send_message(self, instagram_link, user):
        group.messages_set_typing(user)

        if not is_instagram_link(instagram_link):
            group.send_messages(user.id, message='Отправьте пожалуйста ссылку на фото из instagram.com')
            return None

        try:
            for instagram_photo in get_instagram_photos(instagram_link):
                group.messages_set_typing(user)
                group.send_messages(user.id, image_files=[instagram_photo])
        except InstagramError:
            group.send_messages(user.id, message='Не могу найти, возможно фото/видео доступно только для подписчиков (приватный аккаунт)')
