from django.conf.urls import include, url
from django.contrib import admin
from crudbuilder.urls import UrlBuilder

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/',  include('django.contrib.auth.urls')),
]


builder = UrlBuilder('example', 'person')
urlpatterns += builder.urls
