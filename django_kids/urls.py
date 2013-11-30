from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

from links.views import Home

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^links/', include('links.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

#    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    # This is the 2-step authentication backend
    url(r'^accounts/', include('registration.backends.default.urls')),
)

urlpatterns += staticfiles_urlpatterns()