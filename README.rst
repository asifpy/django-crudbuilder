|Build|_ |CodeHealth|_ |coverage|_ |pypi|_ |CodeQuality|_

.. |Build| image:: https://travis-ci.org/asifpy/django-crudbuilder.svg?branch=master
.. _Build: https://travis-ci.org/asifpy/django-crudbuilder

.. |CodeHealth| image:: https://landscape.io/github/asifpy/django-crudbuilder/master/landscape.svg?style=flat
.. _CodeHealth: https://landscape.io/github/asifpy/django-crudbuilder/master

.. |pypi| image:: https://img.shields.io/pypi/v/django-crudbuilder.svg
.. _pypi: https://pypi.python.org/pypi/django-crudbuilder

.. |CodeQuality| image:: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/badges/build.png?b=master
.. _CodeQuality: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/?branch=master

.. |coverage| image:: https://coveralls.io/repos/github/asifpy/django-crudbuilder/badge.svg?branch=master
.. _coverage: https://coveralls.io/github/asifpy/django-crudbuilder?branch=master 


==================
django-crudbuilder
==================

Generic CRUD implementation in Django which uses django tables2 to list objects.

Documentation
-------------

https://django-crudbuilder.readthedocs.org/en/latest/index.html

Features:
---------

- Generates class based views for CRUD
- Uses django-tables2 to display objects in ListView
- Define multiple crud builders for same model with separate URL
- Allows custom forms/tables as additional arguments
- Context provides additional template variables APP_LABEL and MODEL for all CRUD templates
- Enable/disable login required option for CRUD views
- Enable/disable permission required option for CRUD views
- All the generated views/tables/forms/url are extendable.
- post_create and post_update signals to handle specific actions in Create and Update views
- Add your own custom templates for List/Create/Detail/Update/Delete views
- Separate CREATE and UPDATE forms
- Define your own custom queryset for list view
- Inline Formset support for parent child models
- Default Bootstrap3 CSS
- All the generated views are extendable.

Prerequisites
-------------
- Django 1.10+
- Python 2.7+, 3.3+
- Django Tables2 < 2.0

Installation
------------

.. code-block:: python

    pip install django-crudbuilder

Usage
-----

**Add "crudbuilder" to INSTALLED_APPS**

.. code-block:: python

	INSTALLED_APPS = {
		...
		'django_tables2',
		'crudbuilder'
	}

	LOGIN_REQUIRED_FOR_CRUD = True/False
	PERMISSION_REQUIRED_FOR_CRUD = True/False
	PROJECT_NAME = 'YOUR PROJECT NAME'

**Create models in yourapp/models.py**

.. code-block:: python

	class Person(models.Model):
		""" an actual singular human being """
		name = models.CharField(blank=True, max_length=100)
		email = models.EmailField()
		created_at = models.DateTimeField(auto_now=True)
		created_by = models.ForeignKey(User, blank=True, null=True)

		def __unicode__(self):
			return self.name

**Create CRUD for Person model in yourapp/crud.py**

.. code-block:: python

	from crudbuilder.abstract import BaseCrudBuilder
  	from yourapp.models import Person

  	class PersonCrud(BaseCrudBuilder):
  		model = Person
  		search_fields = ['name']
  		tables2_fields = ('name', 'email')
  		tables2_css_class = "table table-bordered table-condensed"
  		tables2_pagination = 20  # default is 10
  		modelform_excludes = ['created_by', 'updated_by']
  		login_required=True
  		permission_required=True
  		# permissions = {
  		#   'list': 'example.person_list',
  		#	'create': 'example.person_create'
  		# }


**Open yourapp/urls.py and add the following**

.. code-block:: python
	
	from crudbuilder import urls

	urlpatterns = [
		url(r'^admin/', include(admin.site.urls)),
		url(r'^crud/',  include(urls)),
	]

**View All your registered CRUDS**

.. code-block:: python

	http://127.0.0.1:8000/crud/


**Now you can access the below CRUD URLS**

.. code-block:: python

	- http://127.0.0.1:8000/crud/yourappname/yourmodelname
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/create/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/detail/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/update/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/delete/


LOGIN REQUIRED
--------------

To enable global login required for all the models CRUD views, add the following to settings file

.. code-block:: python

	LOGIN_REQUIRED_FOR_CRUD = True

If you want to enable login required only for specific model crud, then you need to add following to crud class

	.. code-block:: python
		
		# myapp/crud.py
		login_required = True


PERMISSION REQUIRED
-------------------

To enable global permission required for all the models CRUD views, add the following to settings file

.. code-block:: python

	PERMISSION_REQUIRED_FOR_CRUD = True

If you want to enable permission required only for specific model crud, then you need to add following to crud class

	.. code-block:: python
		
		# myapp/crud.py
		permission_required = True

By enabling either of above flag, crudbuilder by default checks for following permissions:

.. code-block:: python
	
	- For ListView   : <your app_name>.<your model>_list
	- For CreateView : <your app_name>.<your model>_create
	- For DetailView : <your app_name>.<your model>_detail
	- For UpdateView : <your app_name>.<your model>_update
	- For DeleteView : <your app_name>.<your model>_delete


If you want to add your own permissions, then define your own permission required dictionary explicitly in CRUD class.

.. code-block:: python
	
	permissions = {
		'list'  : 'example.permission1',
		'create': 'example.permission2'
		'detail': 'example.permission3',
		'update': 'example.permission4',
		'delete': 'example.permission5',
		}

EXTRA TEMPLATE VARIABLES
------------------------
Added mixin which allows access to additional template variables like app lable and model name in every template.

.. code-block:: python

	APP : {{app_label}}
	MODEL : {{actual_model_name}}
	PLURIZED MODEL : {{pluralized_model_name}}
