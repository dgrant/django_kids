from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from links.views import Home

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^links/', include('links.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

#    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}),

    # This is the 2-step authentication backend
    url(r'^accounts/', include('registration.backends.default.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += staticfiles_urlpatterns()
