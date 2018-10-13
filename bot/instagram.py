import json
from urllib.parse import urljoin, urlsplit

import requests

__all__ = ('Instagram', 'InstagramError')


class InstagramError(Exception):
    pass


class Instagram:
    def __init__(self, instagram_json):
        self.instagram_json = instagram_json

    @classmethod
    def from_url(cls, instagram_url):
        response = requests.get(instagram_url)

        start = '<script type="text/javascript">window._sharedData = {'
        stop = '};</script>'

        start_position = response.text.find(start)
        stop_position = response.text.find(stop)

        start_slice = start_position + len(start)-1
        stop_slice = stop_position + 1

        raw_json = response.text[start_slice:stop_slice]
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


    @staticmethod
    def is_instagram_link(link: str) -> bool:
        url = urlsplit(link)
        if url.netloc in ["www.instagram.com", "instagram.com"]:
            return True

        return False
