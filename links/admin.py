from django.contrib import admin
from models import Link, Category, Url

class UrlAdmin(admin.ModelAdmin):
    fields = ('media_type', 'media_id',)

class LinkAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'category', 'user', 'private',)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Url, UrlAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Category, CategoryAdmin)
