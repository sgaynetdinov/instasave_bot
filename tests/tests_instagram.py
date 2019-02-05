import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

from bot.instagram import Instagram, InstagramLinkError, Instagram404Error


class InstagramTestCase(unittest.TestCase):
    
    def test__is_instagram_link__invalid(self):
        not_instagram_links = [
            'https://ya.ru',
            'google.com',
            'www.example.com/',
        ]
        
        for link in not_instagram_links:
            with self.assertRaises(InstagramLinkError):
                Instagram._is_instagram_link(link)

    def test__is_instagram_link__valid(self):
        instagram_links = [
            'http://instagram.com',
            'https://instagram.com',
            'https://www.instagram.com/',
        ]

        for link in instagram_links:
            self.assertIsNone(Instagram._is_instagram_link(link))
    
    @patch('bot.instagram.urlopen')
    def test_instagram_link_not_found(self, mock):
        url = 'https://instagram.com/not_found/'
        mock.side_effect = HTTPError(url, code=404, msg='', hdrs='', fp=mock)

        with self.assertRaises(Instagram404Error):
            Instagram.from_url(url)

