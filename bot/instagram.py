import json
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import urlopen


__all__ = ('Instagram', 'InstagramError', 'Instagram404Error')


class InstagramError(Exception):
    pass


class Instagram404Error(InstagramError):
    pass


class Instagram:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    @classmethod
    def from_url(cls, instagram_url):
        try:
            response_text = urlopen(instagram_url).read()
        except HTTPError as err:
            if err.code == 404:
                raise Instagram404Error

        start = '<script type="text/javascript">window._sharedData = {'
        stop = '};</script>'

        response_text = response_text.decode()

        start_position = response_text.find(start)
        stop_position = response_text.find(stop)

        start_slice = start_position + len(start)-1
        stop_slice = stop_position + 1

        raw_json = response_text[start_slice:stop_slice]
        instagram_json = json.loads(raw_json)

        return cls(instagram_json)

    def get_photos_url(self):
        content = self.instagram_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']

        image_url_items = []

        if 'edge_sidecar_to_children' in content:
            for edge in content['edge_sidecar_to_children']['edges']:
                image_url_items.append(edge['node']['display_url'])
        else:
            image_url_items.append(content['display_url'])

        return image_url_items

    def get_text(self):
        content = self.instagram_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        text = content['edge_media_to_caption']['edges'][0]['node']['text']

        return text

    @staticmethod
    def is_instagram_link(link: str) -> bool:
        url = urlsplit(link)
        if url.netloc in ["www.instagram.com", "instagram.com"]:
            return True

        return False
