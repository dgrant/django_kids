from django.test import TestCase
from django.core.urlresolvers import reverse

class TestBrowse(TestCase):

    def setUp(self):
        pass

    def test_non_auth(self):
        url = reverse('browse')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
