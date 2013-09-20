from unittest import TestCase
import urllib2

from common import thumbnail
from mock import patch

class ThumbnailTest(TestCase):
    def test_get_youtube_thumbnail(self):
        self.assertEquals(thumbnail.get_youtube_thumbnail('1234'), 'http://img.youtube.com/vi/1234/0.jpg')

    @patch('common.thumbnail.read_from_url')
    def test_get_vimeo_thumbnail(self, readurl_mock):
        readurl_mock.return_value = '[{"thumbnail_large":"bogus_thumbnail_link"}]'
        self.assertEquals(thumbnail.get_vimeo_thumbnail('1234'), 'bogus_thumbnail_link')

    @patch('common.thumbnail.read_from_url')
    def test_get_vimeo_thumbnail_fail(self, readurl_mock):
        readurl_mock.side_effect = Exception("Failed")
        self.assertEquals(thumbnail.get_vimeo_thumbnail('1234'), '')
