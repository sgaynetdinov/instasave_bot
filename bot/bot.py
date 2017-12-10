import io
from urllib.parse import urlsplit, urljoin
import json
import threading

import requests
import vk

from .error import InstagramError
from .config import GROUP_ID, GROUP_TOKEN

api = vk.Api(GROUP_TOKEN)
group = api.get_group(GROUP_ID)


def is_instagram_link(link):
    url = urlsplit(link)
    if url.netloc in ["www.instagram.com", "instagram.com"]:
        return True

    return False


def _get_instagram_response(instagram_link):
    response = requests.get(instagram_link)
    return response.text


def _is_slider(instagram_response_text):
    check_is_slider = 'edge_sidecar_to_children'
    if instagram_response_text.find(check_is_slider) > 0:
        return True
    return False


def _get_url_instagram_slider(instagram_response_text):
    start = '<script type="text/javascript">window._sharedData = {'
    stop = '};</script>'

    start_position = instagram_response_text.find(start)
    stop_position = instagram_response_text.find(stop)

    raw_json = instagram_response_text[start_position + len(start) - 1:stop_position + 1]
    j = json.loads(raw_json)

    edges = j['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
    for edge in edges:
        response = requests.get(edge['node']['display_url'])
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        yield file_like


def get_instagram_photo(instagram_photo_link):
    if not instagram_photo_link.endswith('/'):
        instagram_photo_link += '/'

    url = urljoin(instagram_photo_link, 'media/?size=l')
    response = requests.get(url)
    if not response.ok:
        raise InstagramError()
    file_like = ('photo.jpg', io.BytesIO(response.content))
    return file_like


def send_message(instagram_link, user):
    if not is_instagram_link(instagram_link):
        group.send_messages(user.id, message='Отправьте пожалуйста ссылку на фото из instagram.com')
        return None

    try:
        text = _get_instagram_response(instagram_link)
        if _is_slider(text):
            for instagram_photo in _get_url_instagram_slider(text):
                group.messages_set_typing(user)
                group.send_messages(user.id, image_files=[instagram_photo])
        else:
            instagram_photo = get_instagram_photo(instagram_photo_link=instagram_link)
            group.send_messages(user.id, image_files=[instagram_photo])
    except InstagramError:
        group.send_messages(user.id, message='Не могу найти фото, проверьте пожалуйста ссылку')


class Bot(object):
    def on_post(self, req, resp):
        resp.data = b'ok'
        data = req.context['data']

        if "message_new" == data.get("type"):
            message_object = data['object']
            message_text = message_object['body']
            user_id = message_object['user_id']

            user = api.get_user(user_id)
            group.messages_set_typing(user)

            threading.Thread(target=send_message, args=(message_text, user)).start()

            if user not in group:
                group.messages_set_typing(user)
                group.send_messages(message_object['user_id'], message='Пожалуйста не забудьте подписать на https://vk.com/instasave_bot :v:')
