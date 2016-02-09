from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/',  include('django.contrib.auth.urls')),
    url(r'^crud/',  include('crudbuilder.urls'))
    ]
