from django.db import models
import urllib2
from urllib2 import HTTPError
import json

from common import thumbnail

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import unittest

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

class LinkManager(models.Manager):

    def public_not_owned_by(self, user):
        return self.exclude(user=user).exclude(private=True).prefetch_related('category')

    def public(self):
        return self.select_related().exclude(private=True).prefetch_related('category')

class Link(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    MEDIA_TYPE = Choices(('youtube', 'YouTube'),
                         ('vimeo', 'Vimeo'),
                         ('url', 'URL'),
                        )
    media_type = models.CharField(max_length=50, default='youtube', choices=MEDIA_TYPE)
    media_id = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    thumbnail_url = models.CharField(max_length=256, null=True, blank=True)
    private = models.BooleanField()

    objects = LinkManager()

    def __unicode__(self):
        return self.title

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
        super(Link, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-ctime']


