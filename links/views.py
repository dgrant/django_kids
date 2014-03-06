from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.base import View
from django.views.generic.edit import ModelFormMixin
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth import login

from .models import *
from .forms import LinkForm

class MagicTokenLogin(View):
    def get(self, request, token):
        try:
            magic_token_obj = MagicToken.objects.get(magictoken=token)
        except MagicToken.DoesNotExist:
            raise Http404

        user = magic_token_obj.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mylinks'))
        else:
            return HttpResponseRedirect(reverse('browse'))

class LinkAdd(CreateView):
    model = Link
    form_class = LinkForm
    success_url = '/'

    def form_valid(self, form):
        media_type = form.cleaned_data['media_type']
        media_id = form.cleaned_data['media_id']
        url, _ = Url.objects.get_or_create(media_type=media_type,
                                           media_id=media_id)

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.url = url
        self.object.save()
        form.save_m2m()

        # what happens if new categories already exist?
        new_categories = form.cleaned_data['new_categories']
        new_categories = new_categories.strip()
        if new_categories != '':
            new_categories_list = new_categories.split(',')
            cats = []
            for new_cat in new_categories_list:
                cat = Category()
                cat.name = new_cat.strip()
                cat.save()
                cats.append(cat)
            self.object.category.add(*cats) 

        return super(ModelFormMixin, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LinkAdd, self).dispatch(*args, **kwargs)

class LinkList(ListView):
    """
    A list of a user's own links
    """
    model = Link
    paginate_by = 100
    template_name = 'links/mylinks.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LinkList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = Link.objects.owned_by(self.request.user)
        if self.kwargs.has_key('category_slug'):
            category_slug = self.kwargs['category_slug']
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super(LinkList, self).get_context_data(**kwargs)
        # User must be logged in to get here.
        # Show only the categories for the links for the user that is logged in
        context['categories'] = Category.objects.filter(link__user__id=self.request.user.id).order_by('name').distinct()
        return context

class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('mylinks'))
        else:
            return HttpResponseRedirect(reverse('browse'))

class Browse(ListView):
    model = Link
    paginate_by = 20
    template_name = 'links/browselinks.html'
    context_object_name = 'link_list'

    def dispatch(self, *args, **kwargs):
        return super(Browse, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            # Authenticated, show only other people's not-private links
            qs = Link.objects.public_not_owned_by(self.request.user)
        else:
            # Not authenticated, show all links except private ones
            qs = Link.objects.public()
        if self.kwargs.has_key('category_slug'):
            category_slug = self.kwargs['category_slug']
            qs = qs.filter(category__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super(Browse, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            # Authenticated, show all categories for videos that aren't my own and aren't private
            context['categories'] = Category.objects.exclude(link__private=True).exclude(link__user__id=self.request.user.id).order_by('name')
        else:
            # Not authenticated, show all categories except ones that are
            # confined to private links
            context['categories'] = Category.objects.exclude(link__private=True).order_by('name')
        return context

