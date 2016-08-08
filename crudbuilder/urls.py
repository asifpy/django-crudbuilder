
from django.conf.urls import url
from django.db import connection

from crudbuilder.registry import registry
from crudbuilder.views import ViewBuilder
from crudbuilder import helpers
helpers.auto_discover()

urlpatterns = []

tables = connection.introspection.table_names()

if tables:
    for app_model, base_crud in registry.items():
        app, _ = app_model.split('-')
        model = base_crud.model.__name__.lower()
        viewbuilder = ViewBuilder(app, model, base_crud)

        urls = []
        pluralized = helpers.plural(model)

        list_view = viewbuilder.generate_list_view()
        update_view = viewbuilder.generate_update_view()
        detail_view = viewbuilder.generate_detail_view()
        create_view = viewbuilder.generate_create_view()
        delete_view = viewbuilder.generate_delete_view()

        url_pattern = '{}/{}'.format(app, pluralized)
        if viewbuilder.custom_url_name:
            url_pattern = viewbuilder.custom_url_name

        url_name = '{}-{}'.format(app, model)
        if viewbuilder.custom_url_name:
            url_name = viewbuilder.custom_url_name

        urlpatterns += [
            url(r'^{}/$'.format(url_pattern),
                list_view.as_view(),
                name='{}-list'.format(url_name)),
            url(r'^{}/(?P<pk>\d+)/$'.format(url_pattern),
                detail_view.as_view(),
                name='{}-detail'.format(url_name)),
            url(r'^{}/create/$'.format(url_pattern),
                create_view.as_view(),
                name='{}-create'.format(url_name)),
            url(r'^{}/(?P<pk>\d+)/update/$'.format(url_pattern),
                update_view.as_view(),
                name='{}-update'.format(url_name)),
            url(r'^{}/(?P<pk>\d+)/delete/$'.format(url_pattern),
                delete_view.as_view(),
                name='{}-delete'.format(url_name))
        ]
