from django.test import TestCase
from links.models import Category

#from model_mommy import mommy

class CategoryTest(TestCase):
    def setUp(self):
        self.cat, _ = Category.objects.get_or_create(name='blah')

    def test_slug(self):
        self.assertEquals(self.cat.slug, 'blah')
        

class LinkTest(TestCase):
    pass
