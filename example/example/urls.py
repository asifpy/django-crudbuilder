from django.conf.urls import include, url
from django.contrib import admin
from example.views import(
    MyCustomPersonListView,
    MyCustomPersonCreateView
)

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^mycustom_people/$', MyCustomPersonListView.as_view(), name='mycustom-people'),
    url(r'^mycustom_people/create/$', MyCustomPersonCreateView.as_view(), name='mycustom-create'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^crud/', include('crudbuilder.urls'))
]
