# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Link.url'
        db.delete_column('links_link', 'url')


    def backwards(self, orm):
        # Adding field 'Link.url'
        db.add_column('links_link', 'url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['links']
