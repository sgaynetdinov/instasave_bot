import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from bot.instagram import (Instagram, Instagram404Error, InstagramLinkError,
                           urlopen)


class InstagramEdgeTestCase(unittest.TestCase):
    @patch('bot.instagram.urlopen')
    def test_get_photos_and_video_url__single_photo(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')

        self.assertEqual(len(insta.get_photos_and_video_url()), 1)
        self.assertEqual(insta.get_photos_and_video_url()[0], 'https://scontent-arn2-1.cdninstagram.com/vp/fd5e4107080aac2cad49178a961ae6e2/5D903E1D/t51.2885-19/s320x320/29090066_159271188110124_1152068159029641216_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com')

    @patch('bot.instagram.urlopen')
    def test_get_text(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        
        self.assertEqual(insta.get_text(), "NASA\n\nExplore the universe and discover our home planet with the official NASA Instagram account\nhttp://www.nasa.gov/")

    @patch('bot.instagram.urlopen')
    def test_get_text_if_not_url(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        del insta._content['external_url']
        
        self.assertEqual(insta.get_text(), "NASA\n\nExplore the universe and discover our home planet with the official NASA Instagram account")

    @patch('bot.instagram.urlopen')
    def test_get_text_if_url_is_None(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        insta._content['external_url'] = None
        
        self.assertEqual(insta.get_text(), "NASA\n\nExplore the universe and discover our home planet with the official NASA Instagram account")

    @patch('bot.instagram.urlopen')
    def test_get_text_if_not_full_name(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        del insta._content['full_name']
        
        self.assertEqual(insta.get_text(), "Explore the universe and discover our home planet with the official NASA Instagram account\nhttp://www.nasa.gov/")

    @patch('bot.instagram.urlopen')
    def test_full_name(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        
        self.assertEqual(insta._full_name, "NASA")

    @patch('bot.instagram.urlopen')
    def test_full_name_if_key_error(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        del insta._content['full_name']
        
        self.assertEqual(insta._full_name, "")

    @patch('bot.instagram.urlopen')
    def test_text_empty(self, mock):
        with open('tests/instagram/account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/nasa/')
        insta._content['biography'] = ''

        self.assertEqual(insta.get_text(), 'NASA')
