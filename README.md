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

EXTENDABLE
----------
All the generated views/tables/forms/url are extendable.

```
# GENERATE CRUD CLASSES
------------------------
>>> from crudbuilder.views import ViewBuilder
>>> builder = ViewBuilder('example', 'person')
>>> builder.generate_crud()
>>> builder.classes
{'PersonCreateView': <class 'django.views.generic.edit.PersonCreateView'>,
 'PersonDeleteView': <class 'crudbuilder.views.PersonDeleteView'>,
 'PersonListView': <class 'crudbuilder.views.PersonListView'>, 
 'PersonUpdateView': <class 'django.views.generic.edit.PersonUpdateView'>,
 'PersonDetailView': <class 'crudbuilder.views.PersonDetailView'>
}

# OVERRIDE AUTO GENERATED VIEWS
------------------------------
>>> from crudbuilder.views import ViewBuilder
>>> builder = ViewBuilder('example', 'person')
>>> builder.generate_crud()
>>> PersonListView = builder.classes['PersonListView']
>>> class CustomPersonListView(PersonListView):
>>>		def get_context_data(self, **kwargs):
>>>			context = super(CustomPersonListView, self).get_context_data(**kwargs)
>>>			context['your_template_variable'] = 'Your new template variable'
>>>			return context

>>> PersonCreateView = builder.classes['PersonCreateView']
>>> class CustomPersonCreateView(PersonCreateView):
>>>		def form_valid(self, form):
>>>			object = form.save(commit=False)
>>>			object.user = self.request.user
>>>			return HttpResponseRedirect(reverse('url-name'))

# OVERRIDE AUTO GENERATED TABLE (from django_tables2)
-----------------------------------------------------
>>> from crudbuilder.tables import TableBuilder
>>> builder = TableBuilder('example', 'person')
>>> PersonTable = builder.generate_table()
>>> class CustomPersonTable(PersonTable):
>>>		# add your custom implementation here
```

