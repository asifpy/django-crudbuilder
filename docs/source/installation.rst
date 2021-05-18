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
        name = models.CharField(blank=True, max_length=100)
        email = models.EmailField()
        created_at = models.DateTimeField(auto_now=True)
        created_by = models.ForeignKey(User, blank=True, null=True)

You can optionally set verbose_name and verbose_name_plural in model's Meta class to have custom name in CRUD interface.

Then create the CRUD class for ``Person`` model::

    # tutorial/crud.py
    from crudbuilder.abstract import BaseCrudBuilder

    class PersonCrud(BaseCrudBuilder):
        model = Person
        search_fields = ['name']
        tables2_fields = ('name', 'email')
        tables2_css_class = "table table-bordered table-condensed"
        tables2_pagination = 20  # default is 10
        modelform_excludes = ['created_by', 'updated_by']
        login_required=True
        permission_required=True

        @classmethod
        def custom_queryset(cls, request, **kwargs):
            """Define your own custom queryset for list view"""
            qset = cls.model.objects.filter(created_by=request.user)
            return qset

        @classmethod
        def custom_context(cls, request, context, **kwargs):
            """Define your own custom context for list view"""
            context['custom_data'] = "Some custom data"
            return context

        @classmethod
        def custom_detail_context(cls, request, context, **kwargs):
            """Define your own custom context for detail view"""
            context['custom_data'] = "Some custom data"
            return context

        # permissions = {
        #     'list': 'example.person_list',
        #     'create': 'example.person_create'
        # }
        # createupdate_forms = {
        #     'create': PersonCreateForm,
        #     'update': PersonUpdateForm
        # }

Finally implement the urls for the CRUD::
    
    # tutorail/urls.py
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^crud/',  include('crudbuilder.urls')),
        ]

The above will generate following URL's::
    
    http://127.0.0.1:8000/crud/yourappname/yourmodelname
    http://127.0.0.1:8000/crud/yourappname/yourmodelname/create/
    http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/detail/
    http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/update/
    http://127.0.0.1:8000/crud/yourappname/yourmodelname/<pk>/delete/

View all your registered CRUDS::
    
    http://127.0.0.1:8000/crud/


CRUD class Attributes
---------------------

Usage of all below attributes you can view in `CRUD class of example project`_ on Github.

- **model** -- Actual model name
- **search_fields** -- Search fields for list view
- **custom_postfix_url** -- Your own custom url postfix, if this value set then the resulted URL will become `/crud/appname/<custom_postfix_url>`.
- **tables2_fields** -- Fields which will be used in django-tables2 fields attribute (in list view)
- **tables2_css_class** -- CSS class for list view table (for django-tables2)
- **tables2_pagination** -- By default crudbuilder will set pagination to 10, you can oveeride this value by setting this attribute
- **modelform_excludes** -- Exclude fields for model form
- **detailview_excludes** -- Exclude fields in Deatail view
- **custom_modelform** -- Your custom model form
- **custom_table2** -- Your custom Tables2 class
- **custom_templates** -- Your own custom templates. For more details on custom templates, you can check :doc:`custom templates </templates>`
- **login_required** -- Enable login required for specific model CRUD (by default False)
- **permission_required** -- Enable permission required for specific model CRUD (by default False)
- **permissions** -- By default crudbuilder will generate crud permissions, if you want to define your own permissions then add permissions dictionary on the CRUD class. For more details on permission, you can check :doc:`custom permission </settings>`
- **createupdate_forms** -- Define separate CREATE and UPDATE forms
- **custom_queryset** -- Define your own custom queryset for list view
- **custom_context** -- Define your own custom context for list view
- **inlineformset** -- Define your Inline Formset for parent child relation, you can check :doc:`inline-formset-parent-child-relation </forms>` for more detail.


.. _example project: https://github.com/asifpy/django-crudbuilder/tree/master/example
.. _CRUD class of example project: https://github.com/asifpy/django-crudbuilder/blob/master/example/example/crud.py

