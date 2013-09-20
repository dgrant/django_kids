from django.forms import ModelForm, ModelMultipleChoiceField, CharField
from .models import Link, Category

class LinkForm(ModelForm):
    new_categories = CharField(required=False)

    class Meta:
        model = Link
        fields = ('title', 'text', 'category', 'media_type', 'media_id',
                  'private',)
