from django.forms import ModelForm, ModelMultipleChoiceField, CharField
from .models import Link, Category

class LinkForm(ModelForm):
    new_categories = CharField()

    def __init__(self, user, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
#        self.fields['category'].queryset = Category.objects.filter(linkcategory__user=user).distinct().order_by('name')

    class Meta:
        model = Link
        fields = ('title', 'text', 'category', 'media_type', 'media_id')
