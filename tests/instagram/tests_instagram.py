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
    def test_get_photos_url__multi_photo(self, mock):
        with open('tests/instagram/multi_photo.html_') as fd:
            m = MagicMock() 
            m.read.return_value = fd.read().encode()
            mock.return_value = m
        
        insta = Instagram.from_url('https://www.instagram.com/p/Bq70HOsg0PW/')

        self.assertEqual(len(insta.get_photos_url()), 6)

    @patch('bot.instagram.urlopen')
    def test_get_photos_url__single_photo(self, mock):
        with open('tests/instagram/single_photo.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BrG6aIGIm2V/')
        
        self.assertEqual(len(insta.get_photos_url()), 1)

    @patch('bot.instagram.urlopen')
    def test_get_video_url__single_video(self, mock):
        with open('tests/instagram/single_video.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/Bw2tSDag5Sy/')
        
        self.assertEqual(len(insta.get_photos_url()), 2)
        self.assertEqual(insta.get_photos_url()[0], 'https://instagram.com/n.jpg')
        self.assertEqual(insta.get_photos_url()[1], 'https://scontent.cdninstagram.com/n.mp4')
 
    @patch('bot.instagram.urlopen')
    def test_get_text(self, mock):
        with open('tests/instagram/text.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BoUlST_HIwv/')
        
        self.assertIn('Incoming spacecraft! 🚀', insta.get_text())
        self.assertEqual(len(insta.get_text()), 940)

    @patch('bot.instagram.urlopen')
    def test_text_empty(self, mock):
        with open('tests/instagram/text_empty.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BucgqYLgoaN/')

        self.assertEqual(insta.get_text(), '')

    @patch('bot.instagram.urlopen')
    def test_private_account(self, mock):
        with open('tests/instagram/private_account.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        with self.assertRaises(Instagram404Error):
            Instagram.from_url('https://www.instagram.com/nasa/')

        
