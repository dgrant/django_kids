# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('links_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('links', ['Category'])

        # Adding model 'Link'
        db.create_table('links_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('ctime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('mtime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('links', ['Link'])

        # Adding M2M table for field category on 'Link'
        db.create_table('links_link_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('link', models.ForeignKey(orm['links.link'], null=False)),
            ('category', models.ForeignKey(orm['links.category'], null=False))
        ))
        db.create_unique('links_link_category', ['link_id', 'category_id'])

    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('links_category')

        # Deleting model 'Link'
        db.delete_table('links_link')

        # Removing M2M table for field category on 'Link'
        db.delete_table('links_link_category')

    models = {
        'links.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'links.link': {
            'Meta': {'object_name': 'Link'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['links.Category']", 'symmetrical': 'False'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['links']