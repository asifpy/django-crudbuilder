|Build|_ |CodeHealth|_ |pypi|_ |CodeQuality|_

.. |Build| image:: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/badges/build.png?b=master
.. _Build: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/build-status/master

.. |CodeHealth| image:: https://landscape.io/github/asifpy/django-crudbuilder/master/landscape.svg?style=flat
.. _CodeHealth: https://landscape.io/github/asifpy/django-crudbuilder/master

.. |pypi| image:: https://img.shields.io/pypi/v/django-crudbuilder.svg
.. _pypi: https://pypi.python.org/pypi/django-crudbuilder

.. |CodeQuality| image:: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/badges/quality-score.png?b=master
.. _CodeQuality: https://scrutinizer-ci.com/g/asifpy/django-crudbuilder/?branch=master

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
- Allows custom forms/tables as additional arguments
- Context provides additional template variables APP_LABEL and MODEL for all CRUD templates
- Enable/disable login required option for CRUD views
- Enable/disable permission required option for CRUD views
- All the generated views/tables/forms/url are extendable.
- post_create and post_update signals to handle specific actions in Create and Update views
- Add your own custom templates for List/Create/Detail/Update/Delete views


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
  		search_feilds = ['name']
  		tables2_fields = ('name', 'email')
  		tables2_css_class = "table table-bordered table-condensed"
  		tables2_pagination = 20  # default is 10
  		modelform_excludes = ['created_by', 'updated_by']
  		# permission_required = {
  		#   'list': 'example.person_list',
  		#	'create': 'example.person_create'
  		# }


**Open yourapp/urls.py and add the following**

.. code-block:: python

	urlpatterns = [
		url(r'^admin/', include(admin.site.urls)),
		url(r'^crud/',  include('crudbuilder.urls')),
	]

**Now you can access the below CRUD URLS**

.. code-block:: python

	- http://127.0.0.1:8000/crud/yourappname/yourmodelname
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/create/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/detail/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/update/
	- http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/delete/


LOGIN REQUIRED
--------------

To enable login required for all CRUD views, add the following to settings file

.. code-block:: python

	LOGIN_REQUIRED_FOR_CRUD = True


PERMISSION REQUIRED
-------------------

To enable permission required for all CRUD views, add the following to settings file

.. code-block:: python

	PERMISSION_REQUIRED_FOR_CRUD = True

By enabling the above flag, crudbuilder by default checks for following permissions:

.. code-block:: python
	
	- For ListView   : <your app_name>.<your model>_list
	- For CreateView : <your app_name>.<your model>_create
	- For DetailView : <your app_name>.<your model>_detail
	- For UpdateView : <your app_name>.<your model>_update
	- For DeleteView : <your app_name>.<your model>_delete


If you want to add your own permissions, then define your own permission required dictionary exlicitly in CRUD class.

.. code-block:: python
	
	permission_required = {
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


EXTENDABLE
----------
All the generated views/tables/forms/url are extendable.

.. code-block:: python
	
	# GENERATE CRUD CLASSES
	from crudbuilder.views import ViewBuilder
	builder = ViewBuilder('example', 'person', crudclass)
	builder.generate_crud()
	builder.classes

	{'PersonCreateView': <class 'django.views.generic.edit.PersonCreateView'>,
 	'PersonDeleteView': <class 'crudbuilder.views.PersonDeleteView'>,
 	'PersonListView': <class 'crudbuilder.views.PersonListView'>, 
 	'PersonUpdateView': <class 'django.views.generic.edit.PersonUpdateView'>,
 	'PersonDetailView': <class 'crudbuilder.views.PersonDetailView'>
	}

	# OVERRIDE AUTO GENERATED VIEWS
	from crudbuilder.views import ViewBuilder
	builder = ViewBuilder('example', 'person')
	builder.generate_crud()
	PersonListView = builder.classes['PersonListView']
	class CustomPersonListView(PersonListView):
    	    def get_context_data(self, **kwargs):
        	context = super(CustomPersonListView, self).get_context_data(**kwargs)
        	context['your_template_variable'] = 'Your new template variable'
        	return context

	# OVERRIDE AUTO GENERATED TABLE (from django_tables2)
	from crudbuilder.tables import TableBuilder
	builder = TableBuilder('example', 'person')
	PersonTable = builder.generate_table()
	class CustomPersonTable(PersonTable):
    	    # add your custom implementation here


