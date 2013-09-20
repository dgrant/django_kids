from django.contrib import admin
from models import Link, Category

class LinkAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'category', 'media_type', 'media_id', 'user', 'private',)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Link, LinkAdmin)
admin.site.register(Category, CategoryAdmin)
