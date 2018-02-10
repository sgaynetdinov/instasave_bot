from urllib.parse import urlsplit, urljoin
import requests
import io
import json


__all__ = ('get_instagram_photos', 'is_instagram_link', 'InstagramError')


class InstagramError(Exception):
    pass


def is_instagram_link(link):
    url = urlsplit(link)
    if url.netloc in ["www.instagram.com", "instagram.com"]:
        return True

    return False


def _get_instagram_photos(instagram_response_text):
    start = '<script type="text/javascript">window._sharedData = {'
    stop = '};</script>'

    start_position = instagram_response_text.find(start)
    stop_position = instagram_response_text.find(stop)

    start = start_position + len(start)-1
    stop = stop_position + 1

    raw_json = instagram_response_text[start:stop]
    j = json.loads(raw_json)

    edges = j['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
    for edge in edges:
        response = requests.get(edge['node']['display_url'])
        if not response.ok:
            raise InstagramError()
        file_like = ('photo.jpg', io.BytesIO(response.content))
        yield file_like


def _get_instagram_photo(instagram_photo_link):
    url = urljoin(instagram_photo_link, 'media/?size=l')
    response = requests.get(url)
    if not response.ok:
        raise InstagramError()
    file_like = ('photo.jpg', io.BytesIO(response.content))
    return [file_like]


def _is_slider(instagram_response_text):
    check_is_slider = 'edge_sidecar_to_children'
    if instagram_response_text.find(check_is_slider) > 0:
        return True
    return False


def get_instagram_photos(instagram_photo_link):
    if not instagram_photo_link.endswith('/'):
        instagram_photo_link += '/'

    response = requests.get(instagram_photo_link)
    raw_html = response.text

    if _is_slider(raw_html):
        return _get_instagram_photos(raw_html)
    else:
        return _get_instagram_photo(instagram_photo_link)
