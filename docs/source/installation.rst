Installation and Usage
======================

Install django-crudbuilder::

    pip install django-crudbuilder

Add django-crudbuilder to your ``INSTALLED_APPS``::

    # settings.py
    INSTALLED_APPS = (
        ...
        'django_tables2',
        'crudbuilder'
    )


View the :doc:`additional settings section </settings>` for a list of the django-crudbuilder settings that are available.

For a working implementation, you can view the `example project`_ on Github.

Generating CRUD class based views
---------------------------------

The main business-logic for generating class based views for CRUD is done in ``crudbuilder.views.ViewBuilder()``.  You can use this class method directly in your own Views or you can use one of the Views packaged with this app.


We're going to run through creating a tutorial app. Let's start with a simple model::

    # tutorial/models.py
    class Person(models.Model):
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

Finally implement the urls for the CRUD::
    
    # tutorial/urls.py
    from crudbuilder.urls import UrlBuilder

    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    ]

    builder = UrlBuilder('yourappname', 'yourmodelname')
    urlpatterns += builder.urls

The above will generate following URL's::
    
    http://127.0.0.1:8000/yourappname/yourmodelname
    http://127.0.0.1:8000/yourappname/yourmodelname/create/
    http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/detail/
    http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/update/
    http://127.0.0.1:8000/yourappname/yourmodelname/<pk>/delete/


CRUD Model Attributes
---------------------

- **search_fields** -- Search fields for list view
- **tables2_fields** -- Fields which will be used in django-tables2 fields attribute (in list view)
- **tables2_css_class** -- CSS class for list view table (for django-tables2)
- **tables2_pagination** -- By default crudbuilder will set pagination to 10, you can oveeride this value by setting this attribute
- **modelform_excludes** -- Exclude fields for model form
- **permission_required** -- By default crudbuilder will generate crud permissions, if you want to define your own permissions then add permission_required dictionary on the model. For more details on permission, you can check :doc:`custom permission </settings>`

Usage of all these attributes you can view in `models of example project`_ on Github.

.. _example project: https://github.com/asifpy/django-crudbuilder/tree/master/example
.. _models of example project: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/models.py

