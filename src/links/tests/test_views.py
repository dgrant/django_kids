from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy

class TestBrowse(TestCase):

    def setUp(self):
        pass

    def test_non_auth(self):
        mommy.make('Link', private=False) #1
        mommy.make('Link', private=True)  #2
        mommy.make('Link', private=False) #3

        url = reverse('browse')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)

        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1, 3]))

    def test_category_filter(self):
        mommy.make('Link', private=False) #1
        mommy.make('Link', private=False) #2
        mommy.make('Link', private=False) #3

        url = reverse('browse')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)

        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1, 3]))


    def test_auth(self):
        authuser = User.objects.create_user('test', password='test')
        ret = self.client.login(username='test', password='test')
        self.assertTrue(ret)

        mommy.make('Link', private=False) #1
        mommy.make('Link', private=True)  #2
        mommy.make('Link', private=False) #3
        mommy.make('Link', private=False, user=authuser) #4

        url = reverse('browse')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)
        self.assertNotIn('Login', resp.content)
        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1, 3]))
