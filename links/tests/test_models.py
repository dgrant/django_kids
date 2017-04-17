from django.test import TestCase
from links.models import Category, Link, Url

from django.core.urlresolvers import reverse

from model_mommy import mommy
from mock import Mock, patch

class CategoryTest(TestCase):
    def test_slug(self):
        cat = mommy.make('Category', name='blah')
        self.assertEqual(cat.slug, 'blah')

    def test_unicode(self):
        cat = mommy.make('Category')
        self.assertEqual(str(cat), cat.name)

    def test_get_browse_url(self):
        cat = mommy.make('Category')
        self.assertEqual(cat.get_browse_url(), reverse('browse_category', kwargs={'category_slug': cat.slug}))

    def test_get_mylinks_url(self):
        cat = mommy.make('Category')
        self.assertEqual(cat.get_mylinks_url(), reverse('mylinks_category', kwargs={'category_slug': cat.slug}))

class UrlTest(TestCase):
    @patch('common.thumbnail.get_youtube_thumbnail')
    def test_geturl_youtube(self, thumbnail_mock):
        FAKE_YOUTUBE_THUMB = 'https://fake_youtube_thumbnail_link'
        thumbnail_mock.return_value = FAKE_YOUTUBE_THUMB
        url = mommy.make(Url, media_type='youtube', media_id='12345')
        self.assertEqual(url.get_url(), 'https://www.youtube.com/v/12345?rel=0')

    @patch('common.thumbnail.get_vimeo_thumbnail')
    def test_geturl_vimeo(self, thumbnail_mock):
        FAKE_VIMEO_THUMB = 'https://fake_vimeo_thumbnail_link'
        thumbnail_mock.return_value = FAKE_VIMEO_THUMB
        url = mommy.make(Url, media_type='vimeo', media_id='abcd')
        self.assertEqual(url.get_url(), 'https://vimeo.com/moogaloop.swf?clip_id=abcd')

    def test_geturl_url(self):
        url = mommy.make(Url, media_type='url')
        self.assertEqual(url.get_url(), url.media_id)
        self.assertFalse(url.has_thumbnail())

    @patch('common.thumbnail.get_youtube_thumbnail')
    def test_thumbnail_youtube(self, thumbnail_mock):
        FAKE_YOUTUBE_THUMB = 'https://fake_youtube_thumbnail_link'
        thumbnail_mock.return_value = FAKE_YOUTUBE_THUMB
        url = mommy.make(Url, media_type='youtube')
        self.assertEqual(url.thumbnail_url, FAKE_YOUTUBE_THUMB)
        self.assertTrue(url.has_thumbnail())

    @patch('common.thumbnail.get_vimeo_thumbnail')
    def test_thumbnail_vimeo(self, thumbnail_mock):
        FAKE_VIMEO_THUMB = 'https://fake_vimeo_thumbnail_link'
        thumbnail_mock.return_value = FAKE_VIMEO_THUMB
        url = mommy.make(Url, media_type='vimeo')
        self.assertEqual(url.thumbnail_url, FAKE_VIMEO_THUMB)
        self.assertTrue(url.has_thumbnail())

    def test_url(self):
        url = mommy.make(Url, media_type='url')
        self.assertEqual(url.thumbnail_url, None)
        self.assertFalse(url.has_thumbnail())

    def test_invalid_media_id(self):
        url = mommy.make(Url, media_type='blather')

    def test_unicode(self):
        url = mommy.make(Url, media_type='url')
        self.assertEqual(url.get_url(), str(url))

class UrlManagerTest(TestCase):
    def test_getall(self):
        num_urls = 10
        ids = list(range(1, num_urls+1))
        for i in ids:
            mommy.make('Url')
        with self.assertNumQueries(1):
            self.assertEqual(set(ids), set([x.pk for x in Url.objects.all()]))

class LinkManagerTest(TestCase):
    def setUp(self):
        self.num_links_per_user = 10
        self.actual_ids = list(range(1, 2 * self.num_links_per_user + 1))
        self.user1 = mommy.make('User')
        self.user2 = mommy.make('User')
        for user in (self.user1, self.user2):
            for i in range(1, self.num_links_per_user + 1):
                cat = mommy.make('Category')
                isprivate = i % 2 == 0
                link = mommy.make('Link', private=isprivate, user=user)
                link.category.add(cat)
                link.save()

    def test_public(self):
        """
        Should be one query to prefetch categories
        and one query to get links
        """
        with self.assertNumQueries(2):
            ids = set()
            data = []
            for x in Link.objects.public():
                ids.add(x.pk)
                data.append((x.url, x.category.all(), x.user))
            self.assertEqual(set([x for x in self.actual_ids if (x % 2 == 1)]), ids)

    def test_public_not_owned_by(self):
        """
        Should be one query to prefetch categories
        and one query to get links
        """
        with self.assertNumQueries(2):
            ids = set()
            data = []
            for x in Link.objects.public_not_owned_by(self.user2):
                ids.add(x.pk)
                data.append((x.url, x.category.all()))
            # should only get user1's public links, so links from 1 to num_links_per_user
            self.assertEqual(set([x for x in self.actual_ids if (x % 2 == 1 and x <= self.num_links_per_user)]), ids)

    def test_owned_by(self):
        """
        Should be one query to prefetch categories
        and one query to get links
        """
        with self.assertNumQueries(2):
            ids = set()
            data = []
            for x in Link.objects.owned_by(self.user2):
                ids.add(x.pk)
                data.append((x.url, x.category.all()))
            # should only get user1's links, so links from num_links_per_user + 1 to num_links_per_user * 2
            self.assertEqual(set([x for x in self.actual_ids if (self.num_links_per_user + 1 <= x <= self.num_links_per_user * 2)]), ids)


class LinkTest(TestCase):
    def test_unicode(self):
        url = mommy.make('Url')
        link = mommy.make('Link', url=url)
        self.assertEqual(str(link), link.title + ', ' + str(url))

class MagicTokenTest(TestCase):
    def test_create(self):
        token='adkjupup1343'
        magictoken_obj = mommy.make('MagicToken', magictoken=token)
        self.assertEqual(magictoken_obj.magictoken, token)
