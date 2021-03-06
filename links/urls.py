from django.conf.urls import include, url
from links.views import LinkList, Browse, LinkAdd, MagicTokenLogin

urlpatterns = [
    url(r'^mylinks/$', LinkList.as_view(), name='mylinks'),
    url(r'^mylinks/page(?P<page>[0-9]+)/$', LinkList.as_view()),
    url(r'^mylinks/category/(?P<category_slug>\S+)/$', LinkList.as_view(), name='mylinks_category'),

    url(r'^addlink/$', LinkAdd.as_view(), name='link_add'),

    url(r'^browse/$', Browse.as_view(), name='browse'),
    url(r'^browse/category/(?P<category_slug>\S+)/$', Browse.as_view(), name='browse_category'),

    url(r'^magictokenlogin/([$_0-9a-zA-Z]+)/$', MagicTokenLogin.as_view(), name='magic_token_login'),
]
