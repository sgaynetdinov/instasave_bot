import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from bot.instagram import (Instagram, Instagram404Error, InstagramLinkError,
                           urlopen)


class InstagramEdgeTestCase(unittest.TestCase):
    @patch('bot.instagram.urlopen')
    def test_get_photos_and_video_url__multi_photo(self, mock):
        with open('tests/instagram/multi_photo.html_') as fd:
            m = MagicMock() 
            m.read.return_value = fd.read().encode()
            mock.return_value = m
        
        insta = Instagram.from_url('https://www.instagram.com/p/Bq70HOsg0PW/')

        self.assertEqual(len(insta.get_photos_and_video_url()), 6)

    @patch('bot.instagram.urlopen')
    def test_get_photos_and_video_url__single_photo(self, mock):
        with open('tests/instagram/single_photo.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BrG6aIGIm2V/')
        
        self.assertEqual(len(insta.get_photos_and_video_url()), 1)

    @patch('bot.instagram.urlopen')
    def test_get_video_url__single_video(self, mock):
        with open('tests/instagram/single_video.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/Bw2tSDag5Sy/')
        
        self.assertEqual(len(insta.get_photos_and_video_url()), 2)
        self.assertEqual(insta.get_photos_and_video_url()[0], 'https://instagram.com/n.jpg')
        self.assertEqual(insta.get_photos_and_video_url()[1], 'https://scontent.cdninstagram.com/n.mp4')
 
    @patch('bot.instagram.urlopen')
    def test_get_video_url__multi_video(self, mock):
        with open('tests/instagram/multi_video.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BqsVmrthfF0/')

        self.assertEqual(len(insta.get_photos_and_video_url()), 6)
        self.assertEqual(insta.get_photos_and_video_url()[0], 'https://instagram.com/1.jpg?_nc_ht=instagram.fhel2-1.fna.fbcdn.net')
        self.assertEqual(insta.get_photos_and_video_url()[1], 'https://scontent.cdninstagram.com/1.mp4?_nc_ht=scontent.cdninstagram.com')
        self.assertEqual(insta.get_photos_and_video_url()[2], 'https://instagram.com/2.jpg?_nc_ht=instagram.fhel2-1.fna.fbcdn.net')
        self.assertEqual(insta.get_photos_and_video_url()[3], 'https://scontent.cdninstagram.com/2.mp4?_nc_ht=scontent.cdninstagram.com')
        self.assertEqual(insta.get_photos_and_video_url()[4], 'https://instagram.com/3.jpg?_nc_ht=instagram.fhel2-1.fna.fbcdn.net')
        self.assertEqual(insta.get_photos_and_video_url()[5], 'https://scontent.cdninstagram.com/3.mp4?_nc_ht=scontent.cdninstagram.com')

    @patch('bot.instagram.urlopen')
    def test_get_url__when_both_video_and_photo(self, mock):
        with open('tests/instagram/photo_and_video.html_') as fd:
            m = MagicMock()
            m.read.return_value = fd.read().encode()
            mock.return_value = m

        insta = Instagram.from_url('https://www.instagram.com/p/BvHKqqxBfkf/')

        self.assertEqual(len(insta.get_photos_and_video_url()), 3)
        self.assertEqual(insta.get_photos_and_video_url()[0], 'https://instagram.fhel2-1.fna.fbcdn.net/1.jpg?_nc_ht=instagram.fhel2-1.fna.fbcdn.net')
        self.assertEqual(insta.get_photos_and_video_url()[1], 'https://instagram.fhel2-1.fna.fbcdn.net/2.jpg?_nc_ht=instagram.fhel2-1.fna.fbcdn.net')
        self.assertEqual(insta.get_photos_and_video_url()[2], 'https://scontent.cdninstagram.com/2.mp4?_nc_ht=scontent.cdninstagram.com')
 
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

