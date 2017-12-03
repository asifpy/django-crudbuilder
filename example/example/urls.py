from django.conf.urls import include, url
from django.contrib import admin, auth
from django.db import connection

from crudbuilder import urls

tables = connection.introspection.table_names()

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^crud/', include(urls))
]

if 'django_content_type' in tables:
    from example.views import (
        MyCustomPersonListView,
        MyCustomPersonCreateView
    )

    urlpatterns += [
        url(r'^mycustom_people/$',
            MyCustomPersonListView.as_view(),
            name='mycustom-people'),

        url(r'^mycustom_people/create/$',
            MyCustomPersonCreateView.as_view(),
            name='mycustom-create'),
    ]
