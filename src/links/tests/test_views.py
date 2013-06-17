from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy

class TestBrowse(TestCase):

    def setUp(self):
        pass

    def test_non_auth(self):
        mommy.make('Link')

        url = reverse('browse')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)

        self.assertEquals([link.pk for link in resp.context['link_list']], [1])

