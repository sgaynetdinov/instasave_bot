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


def _get_instagram_photos_url(instagram_response_text):
    start = '<script type="text/javascript">window._sharedData = {'
    stop = '};</script>'

    start_position = instagram_response_text.find(start)
    stop_position = instagram_response_text.find(stop)

    start_slice = start_position + len(start)-1
    stop_slice = stop_position + 1

    raw_json = instagram_response_text[start_slice:stop_slice]
    j = json.loads(raw_json)

    content = j['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    image_url_items = []

    if 'edge_sidecar_to_children' in content:
        for edge in content['edge_sidecar_to_children']['edges']:
            image_url_items.append(edge['node']['display_url'])
    else:
        image_url_items.append(content['display_url'])

    return image_url_items


def _get_photos(urls):
    for url in urls:
        response = requests.get(url)
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        yield file_like


def get_instagram_photos(instagram_photo_link):
    if not instagram_photo_link.endswith('/'):
        instagram_photo_link += '/'

    response = requests.get(instagram_photo_link)
    raw_html = response.text

    photo_urls = _get_instagram_photos_url(raw_html)
    return _get_photos(photo_urls)
