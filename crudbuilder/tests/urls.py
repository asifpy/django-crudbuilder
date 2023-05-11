from django.urls import include, re_path

urlpatterns = [
    re_path(r'^auth/',  include('django.contrib.auth.urls')),
    re_path(r'^crud/',  include('crudbuilder.urls'))
]
