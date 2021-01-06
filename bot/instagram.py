import json
import os
import logging
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

__all__ = ('Instagram', 'InstagramError', 'Instagram404Error', 'InstagramLinkError')


if os.environ.get('SENTRY_ENABLE') == 'On':
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[sentry_logging]
    )


class InstagramError(Exception):
    pass


class Instagram404Error(InstagramError):
    pass


class InstagramLinkError(InstagramError):
    pass


class Instagram:
    @classmethod
    def _is_private(cls, instagram_json):
        return not instagram_json

    @classmethod
    def from_url(cls, instagram_url):
        cls._is_instagram_link(instagram_url)

        try:
            request = Request(urljoin(instagram_url, '?__a=1'))
            request.add_header('Cookie', f'sessionid={os.environ["SESSION_ID"]}')
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36 OPR/18.0.1284.49')
            response_text = urlopen(request).read()
        except HTTPError as err:
            if err.code == 404:
                raise Instagram404Error
            else:
                raise InstagramError

        response_text = response_text.decode()
        try:
            instagram_json = json.loads(response_text)
        except json.JSONDecodeError as err:
            logging.error(err, extra={'response_text': response_text, 'instagram_url': instagram_url})
            raise

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

        return len(path) == 5 and path[2] == 'p' and path[3] != ''

    @classmethod
    def _is_account(cls, link: str) -> bool:
        url = urlsplit(link)

        _path = url.path
        if not _path.endswith('/'):
            _path += '/'

        path = _path.split('/')
        return len(path) == 3 and path[1] != ''

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
        return self.instagram_json['graphql']['shortcode_media']


class InstagramAccount:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    @property
    def _content(self):
        return self.instagram_json['graphql']['user']

    @property
    def _full_name(self):
        try:
            return self._content['full_name']
        except KeyError:
            return ''

    @property
    def _url(self):
        url = None

        try:
            url = self._content['external_url']
        except KeyError:
            pass

        if not url:
            return ''

        return f'\n{url}'

    def get_photos_and_video_url(self):
        return [self._content['profile_pic_url_hd']]

    def get_text(self) -> str:
        if self._full_name and self._content['biography']:
            return self._full_name + '\n\n' + self._content['biography'] + self._url

        if not self._content['biography']:
            return self._full_name

        return self._content['biography'] + self._url


if __name__ == '__main__':
    import sys
    link = sys.argv[1]
    instagram = Instagram.from_url(link)
    text = instagram.get_text()
    print(f'Text: {text}')

    for index, url in enumerate(instagram.get_photos_and_video_url()):
        print(f'Media {index}: {url}')
