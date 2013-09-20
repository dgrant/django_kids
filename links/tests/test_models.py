from django.test import TestCase
from links.models import Category, Link

from django.core.urlresolvers import reverse

from model_mommy import mommy
from mock import Mock, patch

class CategoryTest(TestCase):
    def test_slug(self):
        cat = mommy.make('Category', name='blah')
        self.assertEquals(cat.slug, 'blah')

    def test_unicode(self):
        cat = mommy.make('Category')
        self.assertEquals(unicode(cat), cat.name)

    def test_get_browse_url(self):
        cat = mommy.make('Category')
        self.assertEquals(cat.get_browse_url(), reverse('browse_category', kwargs={'category_slug': cat.slug}))
        
    def test_get_mylinks_url(self):
        cat = mommy.make('Category')
        self.assertEquals(cat.get_mylinks_url(), reverse('mylinks_category', kwargs={'category_slug': cat.slug}))


class LinkTest(TestCase):
    def test_unicode(self):
        link = mommy.make('Link')
        self.assertEquals(unicode(link), link.title)

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

    def test_geturl_url(self):
        link = mommy.make(Link, media_type='url')
        self.assertEquals(link.get_url(), link.media_id)
        self.assertFalse(link.has_thumbnail())

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

    def test_invalid_media_id(self):
        link = mommy.make(Link, media_type='blather')
