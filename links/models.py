from django.db import models
import urllib2
from urllib2 import HTTPError
import json

from common import thumbnail

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import unittest
from django.core.urlresolvers import reverse

from model_utils import Choices

thumbnail_url_cache = {}

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    def get_browse_url(self):
        return reverse('browse_category', kwargs={'category_slug': self.slug})

    def get_mylinks_url(self):
        return reverse('mylinks_category', kwargs={'category_slug': self.slug})


class LinkManager(models.Manager):

    def owned_by(self, user):
        return self.select_related().filter(user=user).prefetch_related('category')

    def public_not_owned_by(self, user):
        return self.exclude(user=user).exclude(private=True).prefetch_related('category')

    def public(self):
        return self.select_related().exclude(private=True).prefetch_related('category')

class Url(models.Model):
    MEDIA_TYPE = Choices(('youtube', 'YouTube'),
                         ('vimeo', 'Vimeo'),
                         ('url', 'URL'),
                        )
    media_type = models.CharField(max_length=50, default='youtube', choices=MEDIA_TYPE)
    media_id = models.CharField(max_length=100, default='')
    thumbnail_url = models.CharField(max_length=256, null=True, blank=True)

    def get_url(self):
        if self.media_type == 'youtube':
            return 'http://www.youtube.com/v/{0}?rel=0'.format(self.media_id)
        elif self.media_type == 'vimeo':
            return 'http://vimeo.com/moogaloop.swf?clip_id={0}'.format(self.media_id)
        elif self.media_type == 'url':
            return self.media_id

    def has_thumbnail(self):
        return self.media_type == 'youtube' or self.media_type == 'vimeo'

    def save(self, *args, **kwargs):
        """ set the thumbnail """
        if self.media_type == 'youtube' or self.media_type == 'vimeo':
            if self.media_type == 'youtube':
                self.thumbnail_url = thumbnail.get_youtube_thumbnail(self.media_id)
            elif self.media_type == 'vimeo':
                self.thumbnail_url = thumbnail.get_vimeo_thumbnail(self.media_id)
        super(Url, self).save(*args, **kwargs)


class Link(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    url = models.ForeignKey(Url)
    user = models.ForeignKey(User)
    private = models.BooleanField()

    objects = LinkManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-ctime']
