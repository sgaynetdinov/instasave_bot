import json
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import urlopen

__all__ = ('Instagram', 'InstagramError', 'Instagram404Error', 'InstagramLinkError')


class InstagramError(Exception):
    pass


class Instagram404Error(InstagramError):
    pass


class InstagramLinkError(InstagramError):
    pass


class Instagram:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    @classmethod
    def _is_private(cls, instagram_json):
        if 'ProfilePage' not in instagram_json['entry_data']:
            return False

        return instagram_json['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']

    @classmethod
    def from_url(cls, instagram_url):
        cls._is_instagram_link(instagram_url)

        try:
            response_text = urlopen(instagram_url).read()
        except HTTPError as err:
            if err.code == 404:
                raise Instagram404Error

        response_text = response_text.decode()
	
        start = '<script type="text/javascript">window._sharedData = '
        stop = ';</script>'

        start_position = response_text.find(start) + len(start)
        stop_position = response_text.find(stop)

        raw_json = response_text[start_position:stop_position]
        instagram_json = json.loads(raw_json)

        if cls._is_private(instagram_json):
            raise Instagram404Error

        return cls(instagram_json)

    def get_photos_url(self):
        image_url_items = []

        if 'edge_sidecar_to_children' in self._content:
            display_url = (edge['node']['display_url'] for edge in self._content['edge_sidecar_to_children']['edges'])
            image_url_items.extend(display_url)
        else:
            image_url_items.append(self._content['display_url'])

        return image_url_items

    def get_text(self) -> str:
        try:
            return self._content['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            return ''

    @property
    def _content(self):
        return self.instagram_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    @classmethod
    def _is_instagram_link(cls, link: str):
        url = urlsplit(link)
        if url.netloc not in ["www.instagram.com", "instagram.com"]:
            raise InstagramLinkError
