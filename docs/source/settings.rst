Additional Settings
===================

There are a few additional settings you can use to add additional functionali for login and permission required and are set in your settings.py file.

LOGIN_REQUIRED_FOR_CRUD
-----------------------

- If ``LOGIN_REQUIRED_FOR_CRUD`` has been marked as ``True`` in settings.py, then login_required decorator will be enabled on all CRUD views globally.
- If you want to enable login required only for specific model crud, then you need to add following to crud class

.. code-block:: python
	
	# myapp/crud.py
	login_required = True

- By default ``LOGIN_REQUIRED_FOR_CRUD`` is ``False``, which means any user can view all the CRUD views.


PERMISSION_REQUIRED_FOR_CRUD
----------------------------

- If ``PERMISSION_REQUIRED_FOR_CRUD`` has been marked as ``True`` in settings.py, then permission_required decorator will be enabled on all CRUD views globally.
- If you want to enable permission required only for specific model crud, then you need to add following to crud class

.. code-block:: python
	
	# myapp/crud.py
	permission_required = True

- By default ``PERMISSION_REQUIRED_FOR_CRUD`` is ``False``, which means any user can view all the CRUD views.

By enabling either of above flag, by default crudbuilder checks for following permissions:

- For ListView   : <your app_name>.<your model>_list
- For CreateView : <your app_name>.<your model>_create
- For DetailView : <your app_name>.<your model>_detail
- For UpdateView : <your app_name>.<your model>_update
- For DeleteView : <your app_name>.<your model>_delete

If you want to add your own permissions, then define your own permission required dictionary exlicitly in CRUD class.::

	permissions = {
    	'list'  : 'example.permission1',
    	'create': 'example.permission2'
    	'detail': 'example.permission3',
    	'update': 'example.permission4',
    	'delete': 'example.permission5',
    	}




