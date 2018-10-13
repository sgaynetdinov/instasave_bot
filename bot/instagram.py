import io
import json
from urllib.parse import urljoin, urlsplit

import requests

__all__ = ('get_instagram_photos', 'is_instagram_link', 'InstagramError')


class InstagramError(Exception):
    pass


def is_instagram_link(link: str) -> bool:
    url = urlsplit(link)
    if url.netloc in ["www.instagram.com", "instagram.com"]:
        return True

    return False


def _get_instagram_photos(instagram_response_text):
    start = '<script type="text/javascript">window._sharedData = {'
    stop = '};</script>'

    start_position = instagram_response_text.find(start)
    stop_position = instagram_response_text.find(stop)

    start_slice = start_position + len(start)-1
    stop_slice = stop_position + 1

    raw_json = instagram_response_text[start_slice:stop_slice]
    j = json.loads(raw_json)

    content = j['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    if 'edge_sidecar_to_children' in content:
        edges = content['edge_sidecar_to_children']['edges']
    else:
        edges = [content['display_url']]

    for edge in edges:
        response = requests.get(edge['node']['display_url'])
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        yield file_like


def get_instagram_photos(instagram_photo_link):
    if not instagram_photo_link.endswith('/'):
        instagram_photo_link += '/'

    response = requests.get(instagram_photo_link)
    raw_html = response.text

    return _get_instagram_photos(raw_html)
