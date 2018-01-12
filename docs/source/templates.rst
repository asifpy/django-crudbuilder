Templates
=========

By default django-crudbuilder uses Bootstrap3 style for its CRUD templates. You can view these templates in `template folder of crudbuilder`_ on Github.


Use your own HTML templates for crudbuilder
-------------------------------------------

You can use your own templates for the crudbuilder in following two ways:

5 common templates for all models CRUD
--------------------------------------

You can create your own 5 common HTML templates for CRUD in templates/crudbuilder, then crudbuilder will use your defined templates.


Model
#####

For single object crud.::

	templates/crudbuilder/instance
		list.html
		create.html
		update.html
		delete.html
		detail.html

Inline Formset
##############

For inline formset.::

	templates/crudbuilder/inline
	    list.html
	    create.html
	    update.html
	    delete.html
	    detail.html


Custom templates for specific model:
######################################

If you want to create custom templates for specific model, then update the CRUD class with custom template path as shown below.::

	class PersonCrud(BaseCrudBuilder):
	    model = Person
	    search_fields = ['name']
	    tables2_fields = ('name', 'email')
	    tables2_css_class = "table table-bordered table-condensed"
	    tables2_pagination = 20  # default is 10
	    modelform_excludes = ['created_by', 'updated_by']

	    custom_templates = {
	        'list': 'yourtemplates/your_list_template.html',
	        'create': 'yourtemplates/your_create_template.html',
	        'detail': 'yourtemplates/your_detail_template.html',
	        'update': 'yourtemplates/your_update_template.html',
	        'delete': 'yourtemplates/your_delete_template.html' 
	        }


Enable search in ListView template
----------------------------------

If you are writing your own custom templates, then please add the following to your list view template to enable the search.::

	<form action="." method="GET">
	    <input type="text" name='search'>
	    <button type="submit" >Search</button>
	</form>


.. _template folder of crudbuilder: https://github.com/asifpy/django-crudbuilder/tree/master/crudbuilder/templates
