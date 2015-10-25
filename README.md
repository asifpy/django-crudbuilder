# django-crudbuilder

Generic CRUD implementation in Django which uses django tables2 to list objects

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

EXTRA TEMPLATE VARIABLES
------------------------
Added mixin which allows access to additional template variables like app lable and model name in every template.

```
APP : {{app_label}}
MODEL : {{actual_model_name}}
PLURIZED MODEL : {{pluralized_model_name}}
```

HELPERS
-------
All the generated views/tables/forms/url are extendable.
[Visit CRUD BUILDER helpers!](https://github.com/asifpy/django-crudbuilder/blob/master/example/example/usage.py)


