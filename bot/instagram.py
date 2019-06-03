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

        if cls._is_edge(instagram_url):
            return InstagramEdge(instagram_json)

        if cls._is_account(instagram_url):
            return InstagramAccount(instagram_json)

    @classmethod
    def _is_edge(cls, link: str) -> bool:
        url = urlsplit(link)
        path = url.path.split('/')

        if len(path) == 4 and path[1] == 'p' and path[2] != '':
            return True

        return False

    @classmethod
    def _is_account(cls, link: str) -> bool:
        url = urlsplit(link)

        _path = url.path
        if not _path.endswith('/'):
            _path += '/'

        path = _path.split('/')
        if len(path) == 3 and path[1] != '':
            return True

        return False

    @classmethod
    def _is_instagram_link(cls, link: str):
        url = urlsplit(link)
        if url.netloc not in ["www.instagram.com", "instagram.com"]:
            raise InstagramLinkError


class InstagramEdge:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    def get_photos_and_video_url(self):
        image_url_items = []

        if 'edge_sidecar_to_children' in self._content:
            node_items = (edge['node'] for edge in self._content['edge_sidecar_to_children']['edges'])
            for node in node_items:
                image_url_items.append(node['display_url'])
                if node['is_video']:
                    image_url_items.append(node['video_url'])
        else:
            image_url_items.append(self._content['display_url'])
            if self._content.get('video_url'):
                image_url_items.append(self._content['video_url'])

        return image_url_items

    def get_text(self) -> str:
        try:
            return self._content['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            return ''

    @property
    def _content(self):
        return self.instagram_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']


class InstagramAccount:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    @property
    def _content(self):
        return self.instagram_json['entry_data']['ProfilePage'][0]['graphql']['user']

    @property
    def _full_name(self):
        try:
            return self._content['full_name']
        except KeyError:
            return ''

    @property
    def _url(self):
        try:
            return '\n' + self._content['external_url']
        except KeyError:
            return ''

    def get_photos_and_video_url(self):
        return [self._content['profile_pic_url_hd']]

    def get_text(self) -> str:
        if self._full_name and self._content['biography']:
            return self._full_name + '\n' + self._content['biography'] + self._url

        if not self._content['biography']:
            return self._full_name

        return self._content['biography'] + self._url
