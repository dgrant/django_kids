from django.test import TestCase
from links.models import Category, Link

from model_mommy import mommy
from mock import Mock, patch

class CategoryTest(TestCase):
    def setUp(self):
        self.cat, _ = Category.objects.get_or_create(name='blah')

    def test_slug(self):
        self.assertEquals(self.cat.slug, 'blah')
        

class LinkTest(TestCase):
    def setUp(self):
        pass

    @patch('common.thumbnail.get_youtube_thumbnail')
    def test_geturl_youtube(self, thumbnail_mock):
        FAKE_YOUTUBE_THUMB = 'http://fake_youtube_thumbnail_link'
        thumbnail_mock.return_value = FAKE_YOUTUBE_THUMB
        link = mommy.make(Link, media_type='youtube', media_id='12345')
        self.assertEquals(link.get_url(), 'http://www.youtube.com/v/12345?rel=0')

    @patch('common.thumbnail.get_vimeo_thumbnail')
    def test_geturl_vimeo(self, thumbnail_mock):
        FAKE_VIMEO_THUMB = 'http://fake_vimeo_thumbnail_link'
        thumbnail_mock.return_value = FAKE_VIMEO_THUMB
        link = mommy.make(Link, media_type='vimeo', media_id='abcd')
        self.assertEquals(link.get_url(), 'http://vimeo.com/moogaloop.swf?clip_id=abcd')

    @patch('common.thumbnail.get_youtube_thumbnail')
    def test_thumbnail_youtube(self, thumbnail_mock):
        FAKE_YOUTUBE_THUMB = 'http://fake_youtube_thumbnail_link'
        thumbnail_mock.return_value = FAKE_YOUTUBE_THUMB
        link = mommy.make(Link, media_type='youtube')
        self.assertEquals(link.thumbnail_url, FAKE_YOUTUBE_THUMB)
        self.assertTrue(link.has_thumbnail())

    @patch('common.thumbnail.get_vimeo_thumbnail')
    def test_thumbnail_vimeo(self, thumbnail_mock):
        FAKE_VIMEO_THUMB = 'http://fake_vimeo_thumbnail_link'
        thumbnail_mock.return_value = FAKE_VIMEO_THUMB
        link = mommy.make(Link, media_type='vimeo')
        self.assertEquals(link.thumbnail_url, FAKE_VIMEO_THUMB)
        self.assertTrue(link.has_thumbnail())

    def test_url(self):
        link = mommy.make(Link, media_type='url')
        self.assertEquals(link.thumbnail_url, None)
        self.assertFalse(link.has_thumbnail())
