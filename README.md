# django-crudbuilder
Generic CRUD implementation in Django

Installation
------------

`pip install django-crudbuilder`

Usage
-----

```
1. Add "crudbuilder" to INSTALLED_APPS:
  INSTALLED_APPS = {
    ...
    'crudbuilder'
  }

2. Open urls.py and add the following

from crudbuilder.urls import UrlBuilder

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

builder = UrlBuilder('yourappname', 'yourmodelname', table_fields=('name', 'email'))
urlpatterns += builder.urls

3. Now you can access the below CRUD URLS:
- http://127.0.0.1:8000/yourappname/yourmodelname
- http://127.0.0.1:8000/yourappname/yourmodelname/create/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/detail/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/update/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/delete/
```
