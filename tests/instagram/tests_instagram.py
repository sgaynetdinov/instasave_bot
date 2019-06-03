import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from bot.instagram import (Instagram, Instagram404Error, InstagramLinkError,
                           urlopen)


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
        url = 'https://www.instagram.com/p/Bq70HOsg0PW/' 
        mock.side_effect = HTTPError(url, code=404, msg='', hdrs='', fp=mock)

        with self.assertRaises(Instagram404Error):
            Instagram.from_url(url)

    @patch('bot.instagram.urlopen')
    def test_private_account(self, mock):
        with open('tests/instagram/private_account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        with self.assertRaises(Instagram404Error):
            Instagram.from_url('https://www.instagram.com/nasa/')

    def test__is_instagam_edge(self):
        url = 'https://www.instagram.com/p/Bq70HOsg0PW/' 
        self.assertTrue(Instagram._is_instagram_edge(url))

        url = 'https://www.instagram.com/p//' 
        self.assertFalse(Instagram._is_instagram_edge(url))

    def test__is_instagram_account(self):
        url = 'https://www.instagram.com/nasa/'
        self.assertTrue(Instagram._is_instagram_account(url))

        url = 'https://www.instagram.com/nasa'
        self.assertTrue(Instagram._is_instagram_account(url))

        url = 'https://www.instagram.com/nasa?q=q'
        self.assertTrue(Instagram._is_instagram_account(url))

        url = 'https://www.instagram.com//'
        self.assertFalse(Instagram._is_instagram_account(url))

