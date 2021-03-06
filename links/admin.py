from django.contrib import admin
from .models import *

class UrlAdmin(admin.ModelAdmin):
    fields = ('media_type', 'media_id',)
    list_display = ('media_id', 'media_type', 'thumbnail_url', )

class LinkAdmin(admin.ModelAdmin):
    fields = ('title', 'comment', 'category', 'user', 'private', 'url')

class CategoryAdmin(admin.ModelAdmin):
    pass

class MagicTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(Url, UrlAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(MagicToken, MagicTokenAdmin)
