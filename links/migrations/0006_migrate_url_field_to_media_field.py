# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for link in orm.Link.objects.exclude(url__icontains='vimeo').exclude(url__icontains='youtu'):
            link.media_type = 'url'
            link.media_id = link.url
            link.save()

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'links.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'links.link': {
            'Meta': {'ordering': "['-ctime']", 'object_name': 'Link'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['links.Category']", 'symmetrical': 'False'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'media_type': ('django.db.models.fields.CharField', [], {'default': "'youtube'", 'max_length': '50'}),
            'mtime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['links']
    symmetrical = True
