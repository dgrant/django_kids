from django import forms
from .models import Link, Category, Url

class LinkForm(forms.ModelForm):
    new_categories = forms.CharField(required=False)
    media_type = forms.ChoiceField(required=True, choices=Url.MEDIA_TYPE)
    media_id = forms.CharField(required=True)

    class Meta:
        model = Link
        fields = ('title', 'comment', 'category', 'private',)
