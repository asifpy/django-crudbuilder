
from django.conf.urls import patterns, url
from crudbuilder.views import ViewBuilder
from crudbuilder import text

class UrlBuilder(object):

    def __init__(self, model):
        self.model = model
        self.viewbuilder = ViewBuilder(self.model)
        self.urls = self.generate_urls()

    def generate_urls(self):
        urls = []

        pluralized = text.plural(self.model)
        
        list_view = self.viewbuilder.generate_list_view()
        update_view = self.viewbuilder.generate_update_view()
        detail_view = self.viewbuilder.generate_detail_view()
        create_view = self.viewbuilder.generate_create_view()
        delete_view = self.viewbuilder.generate_delete_view()

        entries = [
            (r'^{}/$', list_view.as_view(), '{}-list'),
            (r'^{}/(?P<pk>\d+)/$', detail_view.as_view(), '{}-detail'),
            (r'^{}/create/$', create_view.as_view(), '{}-create'),
            (r'^{}/(?P<pk>\d+)/update/$', update_view.as_view(), '{}-update'),
            (r'^{}/(?P<pk>\d+)/delete/$', delete_view.as_view(), '{}-delete'),
        ]

        for entry in entries:
            address = entry[0].format(pluralized)
            url_name = entry[2].format(self.model)

            urls.append(
                url(address, entry[1], name=url_name),
            )
        return urls
