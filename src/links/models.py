from django.db import models
import urllib2
import json

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import unittest

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

LINK_MEDIA_TYPE_CHOICES = (
                           ('youtube', 'YouTube'),
                           ('vimeo', 'Vimeo'),
                           ('url', 'URL'),
                          )


class Link(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    media_type = models.CharField(max_length=50, default='youtube', choices=LINK_MEDIA_TYPE_CHOICES)
    media_id = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User)
    thumbnail_url = models.CharField(max_length=256, null=True, blank=True)
    private = models.BooleanField()

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
        # set the thumbnail
        if self.media_type == 'youtube' or self.media_type == 'vimeo':
            if self.media_type == 'youtube':
                self.thumbnail_url = 'http://img.youtube.com/vi/{0}/0.jpg'.format(self.media_id)
            elif self.media_type == 'vimeo':
                url = 'http://vimeo.com/api/v2/video/{0}.json'.format(self.media_id)
                try:
                    openurl = urllib2.urlopen(url)
                except:
                    print "Failed to fetch url: {0}".format(url)
                    self.thumbnail_url = ''
                else:
                    self.thumbnail_url = json.loads(openurl.read())[0]['thumbnail_large']
        super(Link, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-ctime']

