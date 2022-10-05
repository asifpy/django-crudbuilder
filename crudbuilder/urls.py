
from django.urls import re_path
from django.db import connection
from django.urls import path

from crudbuilder.registry import registry
from crudbuilder.views import ViewBuilder, crudlist_view
from crudbuilder import helpers
helpers.auto_discover()

urlpatterns = [
    re_path(r'^$', crudlist_view, name='crud-index'),
]

tables = connection.introspection.table_names()

if 'django_content_type' in tables:
    for app_model, base_crud in registry.items():

        app, model, postfix_url = app_model.split('-', 2)
        viewbuilder = ViewBuilder(app, model, base_crud)

        urls = []

        list_view = viewbuilder.generate_list_view()
        update_view = viewbuilder.generate_update_view()
        detail_view = viewbuilder.generate_detail_view()
        create_view = viewbuilder.generate_create_view()
        delete_view = viewbuilder.generate_delete_view()

        entries = [
            (r'^{}/{}/$', list_view.as_view(), '{}-{}-list'),
            (r'^{}/{}/create/$', create_view.as_view(), '{}-{}-create'),
            (r'^{}/{}/(?P<pk>[\w-]+)/$', detail_view.as_view(), '{}-{}-detail'),
            (r'^{}/{}/(?P<pk>[\w-]+)/update/$',
                update_view.as_view(),
                '{}-{}-update'),
            (r'^{}/{}/(?P<pk>[\w-]+)/delete/$',
                delete_view.as_view(),
                '{}-{}-delete'),
        ]

        for entry in entries:
            address = entry[0].format(app, postfix_url)
            url_name = entry[2].format(app, postfix_url)

            urls.append(
                re_path(address, entry[1], name=url_name),
            )
        urlpatterns += urls
