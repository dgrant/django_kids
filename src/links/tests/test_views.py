from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from model_mommy import mommy

from links.models import Category

class TestBrowse(TestCase):

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

    def test_category_filter(self):
        link1 = mommy.make('Link', private=False) #1
        cat1 = mommy.make('Category')
        link1.category.add(cat1)
        link1.save()

        link2 = mommy.make('Link', private=True) #2
        link2.category.add(cat1)
        link2.save()

        mommy.make('Link', private=False) #3

        url = reverse('browse_category', kwargs={'category_slug': cat1.slug})
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)

        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1]))


class TestMyLinks(TestCase):
    def test_linklist_unauth(self):
        pass
    
    def test_linklist_auth(self):
        authuser = User.objects.create_user('test', password='test')
        ret = self.client.login(username='test', password='test')
        self.assertTrue(ret)

        mommy.make('Link', private=False, user=authuser) #1
        mommy.make('Link', private=True, user=authuser)  #2
        mommy.make('Link', private=False) #3
        mommy.make('Link', private=True) #4

        url = reverse('mylinks')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)
        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1, 2]))

    def test_linklist_auth_category_filtering(self):
        authuser = User.objects.create_user('test', password='test')
        ret = self.client.login(username='test', password='test')
        self.assertTrue(ret)

        link1 = mommy.make('Link', private=False, user=authuser) #1
        cat1 = mommy.make('Category')
        link1.category.add(cat1)
        link1.save()

        mommy.make('Link', private=True, user=authuser)  #2

        mommy.make('Link', private=False) #3

        link4 = mommy.make('Link', private=True) #4
        link4.category.add(cat1)
        link4.save()

        url = reverse('mylinks_category', kwargs={'category_slug': cat1.slug})

        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertIn('categories', resp.context)
        self.assertIn('link_list', resp.context)
        self.assertEquals(set([link.pk for link in resp.context['link_list']]),
                          set([1]))

    def test_linklist_noauth(self):
        """ should get re-directed to login page at /accounts/login """
        url = reverse('mylinks')
        resp = self.client.get(url)
        self.assertRedirects(resp, 'http://testserver/accounts/login/?next=/links/mylinks/')


class TestHome(TestCase):
    def test_auth_redirect_to_mylinks(self):
        authuser = User.objects.create_user('test', password='test')
        ret = self.client.login(username='test', password='test')
        self.assertTrue(ret)
        url = reverse('home')
        resp = self.client.get(url)
        self.assertRedirects(resp, 'http://testserver/links/mylinks/')

    def test_noauth_redirect_to_mylinks(self):
        url = reverse('home')
        resp = self.client.get(url)
        self.assertRedirects(resp, 'http://testserver/links/browse/')


class TestLinkAdd(TestCase):
    def test_auth(self):
        authuser = User.objects.create_user('test', password='test')
        ret = self.client.login(username='test', password='test')
        self.assertTrue(ret)

        url = reverse('link_add')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)

