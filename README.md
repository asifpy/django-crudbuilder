# django-crudbuilder

[![Build Status](https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/badges/build.png?b=master)](https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/build-status/master) [![Code Health](https://landscape.io/github/asifpy/django-crudbuilder/master/landscape.svg?style=flat)](https://landscape.io/github/asifpy/django-crudbuilder/master) [![PyPI Version](https://img.shields.io/pypi/v/django-crudbuilder.svg)](https://pypi.python.org/pypi/django-crudbuilder) [![Code Quality](https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/?branch=master)


Generic CRUD implementation in Django which uses django tables2 to list objects.

Documentation
-------------

https://django-crudbuilder.readthedocs.org/en/latest/index.html

Features:
---------
- Generates class based views for CRUD
- Uses django-tables2 to display objects in ListView
- Allows custom forms/tables as additional arguments
- Context provides additional template variables APP_LABEL and MODEL for all CRUD templates
- Enable/disable login required option for CRUD views
- Enable/disable permission required option for CRUD views
- All the generated views/tables/forms/url are extendable.
- post_create and post_update signals to handle specific actions in Create and Update views

Installation
------------

`pip install django-crudbuilder`

Usage
-----

1. Add "crudbuilder" to INSTALLED_APPS:
 ``` 
  INSTALLED_APPS = {
    ...
    'django_tables2',
    'crudbuilder'
  }
  
  LOGIN_REQUIRED_FOR_CRUD = True/False
  PERMISSION_REQUIRED_FOR_CRUD = True/False
  ```

2. Create models
``` 
class Person(models.Model):
    """ an actual singular human being """
    
    # for crudbuilder
    search_feilds = ['name']
    tables2_fields = ('name', 'email')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20 # default is 10
    modelform_excludes = ['created_by']
    # permission_required = {
    #     'list': 'example.permission1',
    #     'create': 'example.permission2'
    # }

    # model fields
    name = models.CharField(blank=True, max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.name
``` 

3. Open urls.py and add the following
``` 
from crudbuilder.urls import UrlBuilder

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

builder = UrlBuilder('yourappname', 'yourmodelname')
urlpatterns += builder.urls
``` 

4. Now you can access the below CRUD URLS:
``` 
- http://127.0.0.1:8000/yourappname/yourmodelname
- http://127.0.0.1:8000/yourappname/yourmodelname/create/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/detail/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/update/
- http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/delete/
```

LOGIN REQUIRED
--------------
To enable login required for all CRUD views, add the following to settings file

``` LOGIN_REQUIRED_FOR_CRUD = True```


PERMISSION REQUIRED
-------------------
To enable permission required for all CRUD views, add the following to settings file

``` PERMISSION_REQUIRED_FOR_CRUD = True```

By enabling the above flag, crudbuilder by default checks for following permissions:

``` 
- For ListView   : <your app_name>.<your model>_list
- For CreateView : <your app_name>.<your model>_create
- For DetailView : <your app_name>.<your model>_detail
- For UpdateView : <your app_name>.<your model>_update
- For DeleteView : <your app_name>.<your model>_delete
``` 

If you want to add your own permissions, then define your own permission required dictionary exlicitly on the model.
``` 
permission_required = {
    'list'  : 'example.permission1',
    'create': 'example.permission2'
    'detail': 'example.permission3',
    'update': 'example.permission4',
    'delete': 'example.permission5',
    }
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
from crudbuilder.views import ViewBuilder
builder = ViewBuilder('example', 'person')
builder.generate_crud()
builder.classes

{'PersonCreateView': <class 'django.views.generic.edit.PersonCreateView'>,
 'PersonDeleteView': <class 'crudbuilder.views.PersonDeleteView'>,
 'PersonListView': <class 'crudbuilder.views.PersonListView'>, 
 'PersonUpdateView': <class 'django.views.generic.edit.PersonUpdateView'>,
 'PersonDetailView': <class 'crudbuilder.views.PersonDetailView'>
}

# OVERRIDE AUTO GENERATED VIEWS
------------------------------
from crudbuilder.views import ViewBuilder
builder = ViewBuilder('example', 'person')
builder.generate_crud()
PersonListView = builder.classes['PersonListView']
class CustomPersonListView(PersonListView):
		def get_context_data(self, **kwargs):
			context = super(CustomPersonListView, self).get_context_data(**kwargs)
			context['your_template_variable'] = 'Your new template variable'
			return context

PersonCreateView = builder.classes['PersonCreateView']
class CustomPersonCreateView(PersonCreateView):
		def form_valid(self, form):
			object = form.save(commit=False)
			object.user = self.request.user
			return HttpResponseRedirect(reverse('url-name'))

# OVERRIDE AUTO GENERATED TABLE (from django_tables2)
-----------------------------------------------------
from crudbuilder.tables import TableBuilder
builder = TableBuilder('example', 'person')
PersonTable = builder.generate_table()
class CustomPersonTable(PersonTable):
		# add your custom implementation here
```

